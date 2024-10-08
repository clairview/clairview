# the pb2 files are copied manually from github.com/clairview/proxy-provisioner for now
# this file just manually imports what we import elsewhere
from clairview.temporal.proxy_service.proto.proxy_provisioner_pb2_grpc import ProxyProvisionerServiceStub
from clairview.temporal.proxy_service.proto.proxy_provisioner_pb2 import (
    CreateRequest,
    DeleteRequest,
    StatusRequest,
    READY as CertificateState_READY,
)
