"""
Model exported as python.
Name : GRB-omzettingstool
Group : 
With QGIS : 32205
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Grbomzettingstool(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('selecteerdegoedteleggenthematischelaag', 'Selecteer de goed te leggen thematische laag', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('selecteerdereferentielaag', 'Selecteer de referentielaag', types=[QgsProcessing.TypeVectorAnyGeometry], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('AutomatischOmgezet', 'Automatisch omgezet', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('AfwezigInDeOutput', 'Afwezig in de output', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('GelegenOpOpenbaarDomein', 'Gelegen op openbaar domein', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('HandmatigTeControlerenEnAanTePassen', 'Handmatig te controleren en aan te passen', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(40, model_feedback)
        results = {}
        outputs = {}

        # Fix geometries thematische laag
        alg_params = {
            'INPUT': parameters['selecteerdegoedteleggenthematischelaag'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FixGeometriesThematischeLaag'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Fix geometries referentielaag
        alg_params = {
            'INPUT': parameters['selecteerdereferentielaag'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FixGeometriesReferentielaag'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Add autoincremental field
        alg_params = {
            'FIELD_NAME': 'ID',
            'GROUP_FIELDS': [''],
            'INPUT': outputs['FixGeometriesThematischeLaag']['OUTPUT'],
            'MODULUS': 0,
            'SORT_ASCENDING': True,
            'SORT_EXPRESSION': '',
            'SORT_NULLS_FIRST': False,
            'START': 0,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddAutoincrementalField'] = processing.run('native:addautoincrementalfield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Add geometry attributes referentielaag
        alg_params = {
            'CALC_METHOD': 0,  # Layer CRS
            'INPUT': outputs['FixGeometriesReferentielaag']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddGeometryAttributesReferentielaag'] = processing.run('qgis:exportaddgeometrycolumns', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Overlap analysis referentielaag met thematische laag
        alg_params = {
            'INPUT': outputs['AddAutoincrementalField']['OUTPUT'],
            'LAYERS': outputs['FixGeometriesReferentielaag']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['OverlapAnalysisReferentielaagMetThematischeLaag'] = processing.run('native:calculatevectoroverlaps', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Refactor fields referentielaag
        alg_params = {
            'FIELDS_MAPPING': [{'expression': '"area"','length': 0,'name': 'oppervlakte_referentielaag','precision': 0,'type': 6},{'expression': '"perimeter"','length': 0,'name': 'perimeter_referentielaag','precision': 0,'type': 6}],
            'INPUT': outputs['AddGeometryAttributesReferentielaag']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RefactorFieldsReferentielaag'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Extract by attribute na overlap
        alg_params = {
            'FIELD': 'Fixed geometries_pc',
            'INPUT': outputs['OverlapAnalysisReferentielaagMetThematischeLaag']['OUTPUT'],
            'OPERATOR': 4,  # <
            'VALUE': '75',
            'FAIL_OUTPUT': QgsProcessing.TEMPORARY_OUTPUT,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractByAttributeNaOverlap'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Snap geometries to layer
        alg_params = {
            'BEHAVIOR': 0,  # Prefer aligning nodes, insert extra vertices where required
            'INPUT': outputs['ExtractByAttributeNaOverlap']['OUTPUT'],
            'REFERENCE_LAYER': outputs['FixGeometriesReferentielaag']['OUTPUT'],
            'TOLERANCE': 2,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SnapGeometriesToLayer'] = processing.run('native:snapgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Add geometry attributes na autoincremental field
        alg_params = {
            'CALC_METHOD': 0,  # Layer CRS
            'INPUT': outputs['ExtractByAttributeNaOverlap']['FAIL_OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddGeometryAttributesNaAutoincrementalField'] = processing.run('qgis:exportaddgeometrycolumns', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Create spatial index referentielaag
        alg_params = {
            'INPUT': outputs['RefactorFieldsReferentielaag']['OUTPUT']
        }
        outputs['CreateSpatialIndexReferentielaag'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Refactor fields themalaag
        alg_params = {
            'FIELDS_MAPPING': [{'expression': '"ID"','length': 0,'name': 'ID','precision': 0,'type': 4},{'expression': '"area"','length': 0,'name': 'oppervlakte_themalaag','precision': 0,'type': 6},{'expression': '"perimeter"','length': 0,'name': 'perimeter_themalaag','precision': 0,'type': 6}],
            'INPUT': outputs['AddGeometryAttributesNaAutoincrementalField']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RefactorFieldsThemalaag'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Drop field(s)
        alg_params = {
            'COLUMN': ['oppervlakte_referentielaag','perimeter_referentielaag','JOINarea','JOINperimeter','ID','Fixed geometries_area','Fixed geometries_pc','JOINJOINID','JOINJOINoppervlakte_themalaag','JOINJOINperimeter_themalaag','JOINJOINoppervlakte_referentielaag','JOINJOINperimeter_referentielaag','JOINJOINarea','JOINJOINperimeter','JOINJOINpercentage_overlap','oppervlakte_referentielaag','perimeter_referentielaag','JOINID',' FID','JOINoppervlakte_themalaag','JOINperimeter_themalaag','JOINoppervlakte_referentielaag','JOINperimeter_referentielaag','JOINarea','JOINperimeter','JOINpercentage_overlap','area','perimeter','verhouding','ID_2'],
            'INPUT': outputs['SnapGeometriesToLayer']['OUTPUT'],
            'OUTPUT': parameters['GelegenOpOpenbaarDomein']
        }
        outputs['DropFields'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['GelegenOpOpenbaarDomein'] = outputs['DropFields']['OUTPUT']

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Intersection
        alg_params = {
            'INPUT': outputs['RefactorFieldsThemalaag']['OUTPUT'],
            'INPUT_FIELDS': [''],
            'OVERLAY': outputs['RefactorFieldsReferentielaag']['OUTPUT'],
            'OVERLAY_FIELDS': [''],
            'OVERLAY_FIELDS_PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Intersection'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Add geometry attributes na intersectie
        alg_params = {
            'CALC_METHOD': 0,  # Layer CRS
            'INPUT': outputs['Intersection']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddGeometryAttributesNaIntersectie'] = processing.run('qgis:exportaddgeometrycolumns', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Field calculator
        alg_params = {
            'FIELD_LENGTH': 20,
            'FIELD_NAME': 'percentage_overlap',
            'FIELD_PRECISION': 6,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': '"area" / "oppervlakte_referentielaag"',
            'INPUT': outputs['AddGeometryAttributesNaIntersectie']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Extract by expression
        alg_params = {
            'EXPRESSION': 'percentage_overlap > 0.15',
            'INPUT': outputs['FieldCalculator']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractByExpression'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Buffer
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': -0.2,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': outputs['ExtractByExpression']['OUTPUT'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Buffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # Create spatial index na buffer
        alg_params = {
            'INPUT': outputs['Buffer']['OUTPUT']
        }
        outputs['CreateSpatialIndexNaBuffer'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Join attributes by location
        alg_params = {
            'DISCARD_NONMATCHING': True,
            'INPUT': outputs['CreateSpatialIndexReferentielaag']['OUTPUT'],
            'JOIN': outputs['CreateSpatialIndexNaBuffer']['OUTPUT'],
            'JOIN_FIELDS': [''],
            'METHOD': 0,  # Create separate feature for each matching feature (one-to-many)
            'PREDICATE': [0],  # intersects
            'PREFIX': 'JOIN',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByLocation'] = processing.run('native:joinattributesbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # Dissolve
        alg_params = {
            'FIELD': ['JOINID'],
            'INPUT': outputs['JoinAttributesByLocation']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Dissolve'] = processing.run('native:dissolve', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # Add geometry attributes na dissolve
        alg_params = {
            'CALC_METHOD': 0,  # Layer CRS
            'INPUT': outputs['Dissolve']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddGeometryAttributesNaDissolve'] = processing.run('qgis:exportaddgeometrycolumns', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}

        # Field calculator na dissolve
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'verhouding',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': '"area" / "JOINoppervlakte_themalaag"',
            'INPUT': outputs['AddGeometryAttributesNaDissolve']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorNaDissolve'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(22)
        if feedback.isCanceled():
            return {}

        # verhouding < 1.10
        alg_params = {
            'EXPRESSION': 'verhouding < 1.10',
            'INPUT': outputs['FieldCalculatorNaDissolve']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Verhouding110'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(23)
        if feedback.isCanceled():
            return {}

        # verhouding < 0.9
        alg_params = {
            'EXPRESSION': 'verhouding < 0.9',
            'INPUT': outputs['FieldCalculatorNaDissolve']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Verhouding09'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(24)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value na verhouding < 0.9
        alg_params = {
            'DISCARD_NONMATCHING': True,
            'FIELD': 'ID',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'JOINID',
            'INPUT': outputs['AddAutoincrementalField']['OUTPUT'],
            'INPUT_2': outputs['Verhouding09']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueNaVerhouding09'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(25)
        if feedback.isCanceled():
            return {}

        # verhouding > 0.9
        alg_params = {
            'EXPRESSION': 'verhouding > 0.9',
            'INPUT': outputs['Verhouding110']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Verhouding09'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(26)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'JOINID',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'ID',
            'INPUT': outputs['Verhouding09']['OUTPUT'],
            'INPUT_2': outputs['AddAutoincrementalField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(27)
        if feedback.isCanceled():
            return {}

        # Snap geometries to layer na < 0.9
        alg_params = {
            'BEHAVIOR': 0,  # Prefer aligning nodes, insert extra vertices where required
            'INPUT': outputs['JoinAttributesByFieldValueNaVerhouding09']['OUTPUT'],
            'REFERENCE_LAYER': outputs['FixGeometriesReferentielaag']['OUTPUT'],
            'TOLERANCE': 3,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SnapGeometriesToLayerNa09'] = processing.run('native:snapgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(28)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'ID',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'JOINID',
            'INPUT': outputs['ExtractByAttributeNaOverlap']['FAIL_OUTPUT'],
            'INPUT_2': outputs['AddGeometryAttributesNaDissolve']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': 'JOIN',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(29)
        if feedback.isCanceled():
            return {}

        # verhouding > 1.1
        alg_params = {
            'EXPRESSION': 'verhouding > 1.1',
            'INPUT': outputs['FieldCalculatorNaDissolve']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Verhouding11'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(30)
        if feedback.isCanceled():
            return {}

        # Drop field(s)
        alg_params = {
            'COLUMN': ['oppervlakte_referentielaag','perimeter_referentielaag','JOINID',' FID','JOINoppervlakte_themalaag','JOINperimeter_themalaag','JOINoppervlakte_referentielaag','JOINperimeter_referentielaag','JOINarea','JOINperimeter','JOINpercentage_overlap','area','perimeter','verhouding','ID_2'],
            'INPUT': outputs['SnapGeometriesToLayerNa09']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DropFields'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(31)
        if feedback.isCanceled():
            return {}

        # Select by attribute
        alg_params = {
            'FIELD': 'JOINJOINID',
            'INPUT': outputs['JoinAttributesByFieldValue']['OUTPUT'],
            'METHOD': 0,  # creating new selection
            'OPERATOR': 8,  # is null
            'VALUE': ''
        }
        outputs['SelectByAttribute'] = processing.run('qgis:selectbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(32)
        if feedback.isCanceled():
            return {}

        # Drop field(s)
        alg_params = {
            'COLUMN': ['oppervlakte_referentielaag','perimeter_referentielaag','JOINID',' FID','JOINoppervlakte_themalaag','JOINperimeter_themalaag','JOINoppervlakte_referentielaag','JOINperimeter_referentielaag','JOINarea','JOINperimeter','JOINpercentage_overlap','area','perimeter','verhouding','ID_2'],
            'INPUT': outputs['JoinAttributesByFieldValue']['OUTPUT'],
            'OUTPUT': parameters['AutomatischOmgezet']
        }
        outputs['DropFields'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['AutomatischOmgezet'] = outputs['DropFields']['OUTPUT']

        feedback.setCurrentStep(33)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value na verhouding > 1.1
        alg_params = {
            'DISCARD_NONMATCHING': True,
            'FIELD': 'ID',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'JOINID',
            'INPUT': outputs['AddAutoincrementalField']['OUTPUT'],
            'INPUT_2': outputs['Verhouding11']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueNaVerhouding11'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(34)
        if feedback.isCanceled():
            return {}

        # Extract selected features
        alg_params = {
            'INPUT': outputs['SelectByAttribute']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractSelectedFeatures'] = processing.run('native:saveselectedfeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(35)
        if feedback.isCanceled():
            return {}

        # Drop field(s)
        alg_params = {
            'COLUMN': ['oppervlakte_referentielaag','perimeter_referentielaag','JOINarea','JOINperimeter','Fixed geometries_area','Fixed geometries_pc','JOINJOINID','JOINJOINoppervlakte_themalaag','JOINJOINperimeter_themalaag','JOINJOINoppervlakte_referentielaag','JOINJOINperimeter_referentielaag','JOINJOINarea','JOINJOINperimeter','JOINJOINpercentage_overlap'],
            'INPUT': outputs['ExtractSelectedFeatures']['OUTPUT'],
            'OUTPUT': parameters['AfwezigInDeOutput']
        }
        outputs['DropFields'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['AfwezigInDeOutput'] = outputs['DropFields']['OUTPUT']

        feedback.setCurrentStep(36)
        if feedback.isCanceled():
            return {}

        # Snap geometries to layer na > 1.1
        alg_params = {
            'BEHAVIOR': 0,  # Prefer aligning nodes, insert extra vertices where required
            'INPUT': outputs['JoinAttributesByFieldValueNaVerhouding11']['OUTPUT'],
            'REFERENCE_LAYER': outputs['FixGeometriesReferentielaag']['OUTPUT'],
            'TOLERANCE': 3,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SnapGeometriesToLayerNa11'] = processing.run('native:snapgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(37)
        if feedback.isCanceled():
            return {}

        # Drop field(s)
        alg_params = {
            'COLUMN': ['oppervlakte_referentielaag','perimeter_referentielaag','JOINID',' FID','JOINoppervlakte_themalaag','JOINperimeter_themalaag','JOINoppervlakte_referentielaag','JOINperimeter_referentielaag','JOINarea','JOINperimeter','JOINpercentage_overlap','area','perimeter','verhouding','ID_2'],
            'INPUT': outputs['SnapGeometriesToLayerNa11']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DropFields'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(38)
        if feedback.isCanceled():
            return {}

        # Merge vector layers
        alg_params = {
            'CRS': None,
            'LAYERS': [outputs['DropFields']['OUTPUT'],outputs['DropFields']['OUTPUT']],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MergeVectorLayers'] = processing.run('native:mergevectorlayers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(39)
        if feedback.isCanceled():
            return {}

        # Drop field(s)
        alg_params = {
            'COLUMN': ['layer','path'],
            'INPUT': outputs['MergeVectorLayers']['OUTPUT'],
            'OUTPUT': parameters['HandmatigTeControlerenEnAanTePassen']
        }
        outputs['DropFields'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['HandmatigTeControlerenEnAanTePassen'] = outputs['DropFields']['OUTPUT']
        return results

    def name(self):
        return 'GRB-omzettingstool'

    def displayName(self):
        return 'GRB-omzettingstool'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Grbomzettingstool()
