# the pb2 files are copied manually from github.com/markettor/proxy-provisioner for now
# this file just manually imports what we import elsewhere
from markettor.temporal.proxy_service.proto.proxy_provisioner_pb2_grpc import ProxyProvisionerServiceStub
from markettor.temporal.proxy_service.proto.proxy_provisioner_pb2 import (
    CreateRequest,
    DeleteRequest,
    StatusRequest,
    READY as CertificateState_READY,
)
