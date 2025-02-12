from rest_framework import serializers

from bgp.api.serializers import NestedRelationshipSerializer
from devices.api.serializers import (
    NestedConfigurationSerializer,
    NestedPlatformSerializer,
)
from extras.api.serializers import NestedIXAPISerializer
from net.api.serializers import NestedConnectionSerializer
from peering.enums import BGPGroupStatus, BGPSessionStatus, DeviceStatus
from peering.models import (
    AutonomousSystem,
    BGPGroup,
    Community,
    DirectPeeringSession,
    InternetExchange,
    InternetExchangePeeringSession,
    Router,
    RoutingPolicy,
)
from peering_manager.api import (
    ChoiceField,
    PrimaryModelSerializer,
    SerializedPKRelatedField,
)

from .nested_serializers import *

__all__ = (
    "AutonomousSystemSerializer",
    "AutonomousSystemGenerateEmailSerializer",
    "BGPGroupSerializer",
    "CommunitySerializer",
    "DirectPeeringSessionSerializer",
    "InternetExchangeSerializer",
    "InternetExchangePeeringSessionSerializer",
    "RouterSerializer",
    "RouterConfigureSerializer",
    "RoutingPolicySerializer",
    "NestedAutonomousSystemSerializer",
    "NestedBGPGroupSerializer",
    "NestedCommunitySerializer",
    "NestedDirectPeeringSessionSerializer",
    "NestedInternetExchangeSerializer",
    "NestedInternetExchangePeeringSessionSerializer",
    "NestedRouterSerializer",
    "NestedRoutingPolicySerializer",
)


class AutonomousSystemSerializer(PrimaryModelSerializer):
    import_routing_policies = SerializedPKRelatedField(
        queryset=RoutingPolicy.objects.all(),
        serializer=NestedRoutingPolicySerializer,
        required=False,
        many=True,
    )
    export_routing_policies = SerializedPKRelatedField(
        queryset=RoutingPolicy.objects.all(),
        serializer=NestedRoutingPolicySerializer,
        required=False,
        many=True,
    )
    communities = SerializedPKRelatedField(
        queryset=Community.objects.all(),
        serializer=NestedCommunitySerializer,
        required=False,
        many=True,
    )

    class Meta:
        model = AutonomousSystem
        fields = [
            "id",
            "display",
            "asn",
            "name",
            "comments",
            "irr_as_set",
            "irr_as_set_peeringdb_sync",
            "ipv6_max_prefixes",
            "ipv6_max_prefixes_peeringdb_sync",
            "ipv4_max_prefixes",
            "ipv4_max_prefixes_peeringdb_sync",
            "import_routing_policies",
            "export_routing_policies",
            "communities",
            "prefixes",
            "affiliated",
            "local_context_data",
            "tags",
        ]


class AutonomousSystemGenerateEmailSerializer(serializers.Serializer):
    email = serializers.IntegerField()


class BGPGroupSerializer(PrimaryModelSerializer):
    status = ChoiceField(required=False, choices=BGPGroupStatus)
    import_routing_policies = SerializedPKRelatedField(
        queryset=RoutingPolicy.objects.all(),
        serializer=NestedRoutingPolicySerializer,
        required=False,
        many=True,
    )
    export_routing_policies = SerializedPKRelatedField(
        queryset=RoutingPolicy.objects.all(),
        serializer=NestedRoutingPolicySerializer,
        required=False,
        many=True,
    )
    communities = SerializedPKRelatedField(
        queryset=Community.objects.all(),
        serializer=NestedCommunitySerializer,
        required=False,
        many=True,
    )

    class Meta:
        model = BGPGroup
        fields = [
            "id",
            "display",
            "name",
            "slug",
            "status",
            "import_routing_policies",
            "export_routing_policies",
            "communities",
            "local_context_data",
            "comments",
            "tags",
        ]


class CommunitySerializer(PrimaryModelSerializer):
    class Meta:
        model = Community
        fields = [
            "id",
            "display",
            "name",
            "slug",
            "value",
            "type",
            "local_context_data",
            "comments",
            "tags",
        ]


class DirectPeeringSessionSerializer(PrimaryModelSerializer):
    local_autonomous_system = NestedAutonomousSystemSerializer()
    autonomous_system = NestedAutonomousSystemSerializer()
    bgp_group = NestedBGPGroupSerializer(required=False)
    status = ChoiceField(required=False, choices=BGPSessionStatus)
    relationship = NestedRelationshipSerializer()
    import_routing_policies = SerializedPKRelatedField(
        queryset=RoutingPolicy.objects.all(),
        serializer=NestedRoutingPolicySerializer,
        required=False,
        many=True,
    )
    export_routing_policies = SerializedPKRelatedField(
        queryset=RoutingPolicy.objects.all(),
        serializer=NestedRoutingPolicySerializer,
        required=False,
        many=True,
    )
    router = NestedRouterSerializer(required=False)

    class Meta:
        model = DirectPeeringSession
        fields = [
            "id",
            "display",
            "service_reference",
            "local_autonomous_system",
            "local_ip_address",
            "autonomous_system",
            "bgp_group",
            "ip_address",
            "status",
            "relationship",
            "password",
            "encrypted_password",
            "multihop_ttl",
            "import_routing_policies",
            "export_routing_policies",
            "router",
            "local_context_data",
            "bgp_state",
            "received_prefix_count",
            "advertised_prefix_count",
            "last_established_state",
            "comments",
            "tags",
        ]

    def validate(self, attrs):
        multihop_ttl = attrs.get("multihop_ttl")
        ip_src = attrs.get("local_ip_address")
        ip_dst = attrs.get("ip_address")

        if multihop_ttl == 1 and ip_src and (ip_src.network != ip_dst.network):
            raise serializers.ValidationError(
                f"{ip_src} and {ip_dst} don't belong to the same subnet."
            )

        return super().validate(attrs)


class InternetExchangeSerializer(PrimaryModelSerializer):
    ixapi_endpoint = NestedIXAPISerializer(required=False)
    local_autonomous_system = NestedAutonomousSystemSerializer()
    status = ChoiceField(required=False, choices=BGPGroupStatus)
    import_routing_policies = SerializedPKRelatedField(
        queryset=RoutingPolicy.objects.all(),
        serializer=NestedRoutingPolicySerializer,
        required=False,
        many=True,
    )
    export_routing_policies = SerializedPKRelatedField(
        queryset=RoutingPolicy.objects.all(),
        serializer=NestedRoutingPolicySerializer,
        required=False,
        many=True,
    )
    communities = SerializedPKRelatedField(
        queryset=Community.objects.all(),
        serializer=NestedCommunitySerializer,
        required=False,
        many=True,
    )

    class Meta:
        model = InternetExchange
        fields = [
            "id",
            "display",
            "peeringdb_ixlan",
            "ixapi_endpoint",
            "name",
            "slug",
            "status",
            "local_autonomous_system",
            "comments",
            "import_routing_policies",
            "export_routing_policies",
            "communities",
            "local_context_data",
            "tags",
        ]


class InternetExchangePeeringSessionSerializer(PrimaryModelSerializer):
    autonomous_system = NestedAutonomousSystemSerializer()
    ixp_connection = NestedConnectionSerializer()
    status = ChoiceField(required=False, choices=BGPSessionStatus)
    import_routing_policies = SerializedPKRelatedField(
        queryset=RoutingPolicy.objects.all(),
        serializer=NestedRoutingPolicySerializer,
        required=False,
        many=True,
    )
    export_routing_policies = SerializedPKRelatedField(
        queryset=RoutingPolicy.objects.all(),
        serializer=NestedRoutingPolicySerializer,
        required=False,
        many=True,
    )

    class Meta:
        model = InternetExchangePeeringSession
        fields = [
            "id",
            "display",
            "service_reference",
            "autonomous_system",
            "ixp_connection",
            "ip_address",
            "status",
            "password",
            "encrypted_password",
            "multihop_ttl",
            "is_route_server",
            "import_routing_policies",
            "export_routing_policies",
            "local_context_data",
            "bgp_state",
            "received_prefix_count",
            "advertised_prefix_count",
            "last_established_state",
            "comments",
            "tags",
        ]


class RouterSerializer(PrimaryModelSerializer):
    poll_bgp_sessions_last_updated = serializers.DateTimeField(read_only=True)
    configuration_template = NestedConfigurationSerializer(required=False)
    local_autonomous_system = NestedAutonomousSystemSerializer()
    platform = NestedPlatformSerializer()
    status = ChoiceField(required=False, choices=DeviceStatus)

    class Meta:
        model = Router
        fields = [
            "id",
            "display",
            "name",
            "hostname",
            "platform",
            "status",
            "encrypt_passwords",
            "poll_bgp_sessions_state",
            "poll_bgp_sessions_last_updated",
            "configuration_template",
            "local_autonomous_system",
            "netbox_device_id",
            "use_netbox",
            "local_context_data",
            "napalm_username",
            "napalm_password",
            "napalm_timeout",
            "napalm_args",
            "comments",
            "tags",
        ]


class RouterConfigureSerializer(serializers.Serializer):
    routers = serializers.ListField(child=serializers.IntegerField())
    commit = serializers.BooleanField()


class RoutingPolicySerializer(PrimaryModelSerializer):
    class Meta:
        model = RoutingPolicy
        fields = [
            "id",
            "display",
            "name",
            "slug",
            "type",
            "weight",
            "address_family",
            "local_context_data",
            "comments",
            "tags",
        ]
