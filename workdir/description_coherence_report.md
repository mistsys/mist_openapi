# OpenAPI Description Coherence Report

Spec: `openapi.yaml`

This report is heuristic. Review findings before changing the spec, especially conditional wording such as `Required if ...`.

## Summary

- Total heuristic findings: 32
- Missing Schema Descriptions: 0
- Missing Property Descriptions: 0
- Very Short Descriptions: 0
- Descriptions Starting With Property Name: 0
- Defaulted Fields Mentioning Required: 28
- Required Fields Mentioning Optional: 0
- Shape Wording Review: 4
- Repeated description groups: 72

## Terminology Variants

### Preferred: `MAC address`

- Preferred occurrences: 393
- Variant occurrences: 26
- `MAC Address`: 22
  - `tags.69`: "NAC Portals are for onboard Wireless and Wired client with 802.1X The NAC Portal is a web-based interface that allows users to authenticate and gain access to the network. It is typically used for guest access or for devices that do not have a pre-configured certificate for 802.1X authentication. It can also be used to provision certificates for devices that require them with the Mist Application. ### NAC-Based External Guest Portal Authorization / How to implement a External Guest Portal ###..."
  - `paths./api/v1/installer/orgs/{org_id}/devices/{fpc0_mac}/vc.parameters.1`: "FPC0 MAC Address"
  - `paths./api/v1/orgs/{org_id}/devices/search.get.parameters.27`: "When `type`==`gateway`, node0 MAC Address"
- `mac address`: 4
  - `paths./api/v1/orgs/{org_id}/stats/ports/count.get.parameters.10`: "Interface mac address"
  - `paths./api/v1/orgs/{org_id}/stats/ports/search.get.parameters.15`: "Interface mac address"
  - `paths./api/v1/sites/{site_id}/stats/ports/count.get.parameters.10`: "Interface mac address"

### Preferred: `IP address`

- Preferred occurrences: 154
- Variant occurrences: 26
- `IP Address`: 21
  - `paths./api/v1/sites/{site_id}/devices/{device_id}/show_ospf_interfaces.post`: "Get OSPF interfaces from SSR and SRX. The output will be available through websocket. As there can be multiple commands issued against the same device at the same time and the output all goes through the same websocket stream, `session` is introduced for demux. #### Subscribe to Device Command outputs `WS /api-ws/v1/stream` ```json { \"subscribe\": \"/sites/{site_id}/devices/{device_id}/cmd\" } ``` #### Example output from ws stream ``` ===== ================== =================== ============== ..."
  - `components.parameters.partial_filter_ip_client`: "Partial / full Client IP Address. Use `prefix*` for prefix search or `*substring*` for contains search (e.g. `10.100.10.*` and `*100.10.*` match `10.100.10.54`). Suffix-only wildcards (e.g. `*.54`) are not supported"
  - `components.parameters.partial_filter_ip_device`: "Partial / full Device IP Address. Use `prefix*` for prefix search or `*substring*` for contains search (e.g. `10.100.10.*` and `*100.10.*` match `10.100.10.54`). Suffix-only wildcards (e.g. `*.54`) are not supported"
- `ip address`: 5
  - `paths./api/v1/orgs/{org_id}/devices/count.get.parameters.13`: "LLDP management ip address"
  - `paths./api/v1/orgs/{org_id}/devices/search.get.parameters.17`: "When `type`==`ap`, LLDP management ip address"
  - `paths./api/v1/sites/{site_id}/devices/search.get.parameters.17`: "When `type`==`ap`, LLDP management ip address"

### Preferred: `VLAN ID`

- Preferred occurrences: 72
- Variant occurrences: 14
- `VLAN id`: 4
  - `components.schemas.ap_ip_config.vlan_id`: "Management VLAN id, default is 1 (untagged)"
  - `components.schemas.ap_switch_setting_port_vlan_id`: "Native VLAN id, optional"
  - `components.schemas.stats_wireless_client.vlan_id`: "VLAN id, could be empty (from older AP)"
- `Vlan ID`: 9
  - `paths./api/v1/orgs/{org_id}/nac_clients/count.get.parameters.4`: "Vlan ID"
  - `paths./api/v1/orgs/{org_id}/nac_clients/events/search.get.parameters.23`: "Vendor specific Vlan ID in radius requests"
  - `paths./api/v1/orgs/{org_id}/nac_clients/search.get.parameters.20`: "Vendor specific Vlan ID in radius requests"
- `vlan id`: 1
  - `components.schemas.ap_port_config.vlan_id`: "Optional to specify the vlan id for a tunnel if forwarding is for `wxtunnel`, `mxtunnel` or `site_mxedge`. * if vlan_id is not specified then it will use first one in vlan_ids[] of the mxtunnel. * if forwarding == site_mxedge, vlan_ids comes from site_mxedge (`mxtunnels` under site setting)"

### Preferred: `RADIUS`

- Preferred occurrences: 193
- Variant occurrences: 24
- `Radius`: 17
  - `tags.104`: "NAC User MACs (Endpoints) provide a database of endpoints identified by their MAC addresses. They can be used assign each endpoint with various attributes, such as name, VLAN, role and client label. Once an endpoint is labeled, the label name can be used to create [NAC Tags]($h/Orgs%20NAC%20Tags/_overview) as match criteria. [NAC Tags]($h/Orgs%20NAC%20Tags/_overview) can be used to create Tags regrouping one or multiple endpoint MAC Addresses, but the use of the User MACs provides additional ..."
  - `paths./api/v1/orgs/{org_id}/nac_clients/events/search.get.parameters.12`: "Radius attributes returned by NAC to NAS derive"
  - `paths./api/v1/sites/{site_id}/devices/{device_id}/check_radius_server.post`: "Ping test from the AP to confirm 'reachability' of the Radius server. Utilize Juniper EX switch(to which an AP is connected to) radius test capabilities to get details on the Radius Server 'availability'. #### Subscribe to Device Command outputs `WS /api-ws/v1/stream` ```json { \"subscribe\": \"/sites/{site_id}/devices/{device_id}/cmd\" } ``` #### Example output from ws stream ```json { \"event\": \"data\", \"channel\": \"/sites/d6fb4f96-3ba4-4cf5-8af2-a8d7b85087ac/devices/00000000-0000-0000-1000-209339..."
- `radius server`: 7
  - `components.schemas.junos_local_port_config.server_reject_network`: "Only if `port_auth`==`dot1x` when radius server reject / fails"
  - `components.schemas.mxcluster_radsec_server_selection`: "When ordered, Mist Edge will prefer and go back to the first radius server if possible. enum: `ordered`, `unordered`"
  - `components.schemas.radius_config.acct_interim_interval`: "How frequently should interim accounting be reported, 60-65535. default is 0 (use one specified in Access-Accept request from RADIUS Server). Very frequent messages can affect the performance of the radius server, 600 and up is recommended when enabled"

### Preferred: `IPsec`

- Preferred occurrences: 35
- Variant occurrences: 53
- `IPSec`: 6
  - `tags.111`: "A WxLan Tunnel (WxTunnel) are used to create a secure connection between Juniper Mist Access Points and third-party VPN concentrators using protocols such as L2TPv3 or dmvpn. These tunnels allow for the aggregation of ethernet interfaces on access points, support dynamic or static tunnels, and provide options for IPSec encryption."
  - `tags.174`: "A WxLan Tunnel (WxTunnel) are used to create a secure connection between Juniper Mist Access Points and third-party VPN concentrators using protocols such as L2TPv3 or dmvpn. These tunnels allow for the aggregation of ethernet interfaces on access points, support dynamic or static tunnels, and provide options for IPSec encryption."
  - `paths./api/v1/orgs/{org_id}/setting/jse/setup.post`: "In JSE UI: 1. Create custom role with Read access to service_location and RW access to site and IPSec profile APIs. 2. Create a user with the above custom role. - email: john@abc.com 3. Activate the user in the JSE account. 4. Create the service locations on the JSE account."
- `ipsec`: 47
  - `components.schemas.capture_mxedge.mxedges`: "Dict of Mist Edges to capture on, property key is the Mist Edge ID. Property value is a dict of interfaces to capture for the given mxedge (e.g. port1, kni0, lacp0, ipsec, drop, oobm)"
  - `components.schemas.capture_mxedge_mxedges_interfaces`: "Property key is the Port name (e.g. \"port1\", \"kni0\", \"lacp0\", \"ipsec\", \"drop\", \"oobm\"), currently limited to specifying one interface per mxedge"
  - `components.schemas.stats_gateway_vpn_peer.type`: "VPN implementation type for the peer, such as `ipsec` for SRX or `svr` for SSR"

### Preferred: `Mist Edge`

- Preferred occurrences: 327
- Variant occurrences: 46
- `MX Edge`: 1
  - `paths./api/v1/const/mxedge_events.get`: "Get List of available MX Edge Events"
- `MxEdge`: 24
  - `tags.64`: "A Mist Edge (MxEdge) is a physical or virtual appliance that is deployed in a network to provide centralized data path for user traffic or as a RADIUS Proxy, which was traditionally performed by legacy wireless controllers. It keeps all the control and management functions in the Mist Cloud, offering a microservices architecture to the campus."
  - `paths./api/v1/orgs/{org_id}/mxclusters.get`: "Get List of Org MxEdge Clusters"
  - `paths./api/v1/orgs/{org_id}/mxclusters/{mxcluster_id}.get`: "Get Org MxEdge Cluster Details"
- `mxedge`: 21
  - `paths./api/v1/orgs/{org_id}/mxedges/{mxedge_id}/image/{image_number}.post`: "Attach up to 3 images to a mxedge"
  - `paths./api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metric/{metric}/impact-summary.get`: "Get impact summary counts optionally filtered by classifier and failure type * Wireless SLE Fields: `wlan`, `device_type`, `device_os` ,`band`, `ap`, `server`, `mxedge` * Wired SLE Fields: `switch`, `client`, `vlan`, `interface`, `chassis` * WAN SLE Fields: `gateway`, `client`, `interface`, `chassis`, `peer_path`, `gateway_zones`"
  - `webhooks.mxedge_events.post.requestBody`: "Webhook sample for `mxedge-events` topic"

## Missing Schema Descriptions

Count: 0


## Missing Property Descriptions

Count: 0


## Very Short Descriptions

Count: 0


## Descriptions Starting With Property Name

Count: 0


## Defaulted Fields Mentioning Required

Count: 28

- `components.schemas.ap_aeroscout.host`: Defaulted field description mentions required; review for semantic accuracy.
  - Description: "Required if enabled, aeroscout server host"
- `components.schemas.ap_airista.host`: Defaulted field description mentions required; review for semantic accuracy.
  - Description: "Required if enabled, Airista server host"
- `components.schemas.ble_config.power`: Defaulted field description mentions required; review for semantic accuracy.
  - Description: "Required if `power_mode`==`custom`; else use `power_mode` as default"
- ... 25 more

## Required Fields Mentioning Optional

Count: 0


## Shape Wording Review

Count: 4

- `components.schemas.capture_gateway.gateways`: Object-shaped property description uses list/array wording.
  - Description: "List of SSRs. Property key is the SSR MAC"
- `components.schemas.const_device_ap.disallowed_channels`: Object-shaped property description uses list/array wording.
  - Description: "Property key is a list of country codes (e.g. \"GB, DE\")"
- `components.schemas.gateway_template.port_config`: Object-shaped property description uses list/array wording.
  - Description: "Property key is the Port Name (i.e. \"ge-0/0/0\"), the Ports Range (i.e. \"ge-0/0/0-10\"), the List of Ports (i.e. \"ge-0/0/0,ge-1/0/0\", only allowed for Aggregated or Redundant interfaces) or a Variable (i.e. \"{{myvar}}\")."
- ... 1 more

## Repeated Descriptions

Identical descriptions are not automatically bad, but large groups often expose generic wording or reusable concepts.

- 30 uses: "Return a 200 status to indicate that the data was received successfully"
  - `webhooks.alarms.post.responses.200`
  - `webhooks.asset_raw_rssi.post.responses.200`
  - `webhooks.audits.post.responses.200`
  - `webhooks.client_info.post.responses.200`
  - `webhooks.client_join.post.responses.200`
  - `webhooks.client_latency.post.responses.200`
  - `webhooks.client_sessions.post.responses.200`
  - `webhooks.device_events.post.responses.200`
  - ... 22 more
- 12 uses: "All attributes are optional"
  - `paths./api/v1/sites/{site_id}/devices/{device_id}/clear_mac_table.post.requestBody`
  - `paths./api/v1/sites/{site_id}/devices/{device_id}/show_arp.post.requestBody`
  - `paths./api/v1/sites/{site_id}/devices/{device_id}/show_bgp_summary.post.requestBody`
  - `paths./api/v1/sites/{site_id}/devices/{device_id}/show_dot1x.post.requestBody`
  - `paths./api/v1/sites/{site_id}/devices/{device_id}/show_evpn_database.post.requestBody`
  - `paths./api/v1/sites/{site_id}/devices/{device_id}/show_forwarding_table.post.requestBody`
  - `paths./api/v1/sites/{site_id}/devices/{device_id}/show_mac_table.post.requestBody`
  - `paths./api/v1/sites/{site_id}/devices/{device_id}/show_ospf_database.post.requestBody`
  - ... 4 more
- 11 uses: "Whether resolve the site variables"
  - `paths./api/v1/sites/{site_id}/aptemplates/derived.get.parameters.0`
  - `paths./api/v1/sites/{site_id}/deviceprofiles/derived.get.parameters.0`
  - `paths./api/v1/sites/{site_id}/gatewaytemplates/derived.get.parameters.0`
  - `paths./api/v1/sites/{site_id}/networks/derived.get.parameters.0`
  - `paths./api/v1/sites/{site_id}/networktemplates/derived.get.parameters.0`
  - `paths./api/v1/sites/{site_id}/rftemplates/derived.get.parameters.0`
  - `paths./api/v1/sites/{site_id}/secintelprofiles/derived.get.parameters.0`
  - `paths./api/v1/sites/{site_id}/servicepolicies/derived.get.parameters.0`
  - ... 3 more
- ... 69 more groups

