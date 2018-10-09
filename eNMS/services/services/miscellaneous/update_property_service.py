from multiprocessing.pool import ThreadPool
from sqlalchemy import Column, ForeignKey, Integer, PickleType
from sqlalchemy.ext.mutable import MutableDict

from eNMS import db
from eNMS.services.models import Service, service_classes


class UpdatePropertyService(Service):

    __tablename__ = 'UpdatePropertyService'

    id = Column(Integer, ForeignKey('Service.id'), primary_key=True)
    update_dictionnary = Column(MutableDict.as_mutable(PickleType), default={})

    __mapper_args__ = {
        'polymorphic_identity': 'update_property_service',
    }

    def job(self, task, incoming_payload):
        targets = task.compute_targets()
        results = {'success': True, 'devices': {}}
        pool = ThreadPool(processes=len(targets))
        pool.map(
            self.update_property,
            [(task, device, incoming_payload, results) for device in targets])
        pool.close()
        pool.join()
        return results

    def update_property(self, args):
        task, device, payload, results = args
        try:
            for property, value in self.update_dictionnary.items():
                setattr(device, property, value)
            result, success = f'update successfully executed', False
        except Exception as e:
            result, success = f'task failed ({e})', False
            results['success'] = False
        results['devices'][device.name] = {
            'success': success,
            'result': result
        }


service_classes['Update Property Service'] = UpdatePropertyService