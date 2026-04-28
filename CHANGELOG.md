# Changelog

All notable changes to this project will be documented in this file.

## [2602.1.14] - 2026-04-28

- Updated `evpn_options` schema:
  - Added `enable_inband_mgmt` (boolean, default: `false`) — whether to route management traffic inband; routes will be propagated to downstream switches

## [2602.1.13] - 2026-04-28

- Updated `switch_port_config_overwrite` schema:
  - Added `poe_keep_state_when_reboot` (boolean, default: `false`) — whether Perpetual PoE is enabled; keeps PoE state across reboots

## [2602.1.12] - 2026-04-28

- Updated `ap_mesh` schema:
  - Added `use_wpa3_on_5` (boolean, default: `false`) — whether to use WPA3 on the 5 GHz band for mesh links
- Added `ap_zigbee` schema with fields: `enabled`, `channel` (0 = auto, 11–26 for fixed), `pan_id`, `extended_pan_id`, `allow_join`
- Added `ap_zigbee_allow_join` enum schema (`manual` (default), `always`)
- Added `zigbee_config` field (ref: `ap_zigbee`) to `device_ap` and `deviceprofile_ap` schemas

## [2602.1.11] - 2026-04-28

- Updated `stats_asset` schema (Subscribe to BLE Assets Stream):
  - Added `_ttl` (integer) — time-to-live in seconds for the asset data in cache
  - Added `by` (string) — source type (e.g. "asset")
  - Added `device_id` (string UUID, readOnly) — device ID of the loudest AP
  - Added `id` (UUID, readOnly) — unique identifier for the asset
  - Added `manufacture` (string) — manufacturer name resolved from company ID
  - Added `mfg_company_id` (integer) — BLE manufacturer company ID from advertisement
  - Added `mfg_data` (string) — manufacturer-specific data (hex encoded)
  - Added `service_packets` (array, max 10) — list of service data advertisements; each item has `uuid`, `data`, `rx_cnt`, `last_rx_time`
  - Updated `rssi` description to clarify it is the RSSI of the loudest AP
- Added `stats_asset_service_packet` schema
- Added `stats_asset_service_packets` schema
- Updated `AssetStatsExample` and `AssetsArrayStatsExample` with all new fields
- Updated `GET /api/v1/sites/{site_id}/stats/assets` description to include WebSocket subscribe info for BLE Assets Stream (`/sites/:site_id/stats/maps/:map_id/assets`)

- Updated `wlan_auth` schema:
  - Added `enable_gcmp256` (boolean, default: `false`) — enable GCMP-256 encryption suite; default false for better compatibility
  - Added `enable_beacon_protection` (boolean, default: `false`) — enable Beacon Protection; default false for better compatibility

- Updated `marvis_client` schema and Marvis Client Invite endpoints:
  - Added `telemetry` object with `enabled` (boolean) — note: some stats not collected when not connected to Mist infrastructure
  - Added `location` object with `enabled` (boolean)
  - Added `synthetic_test` object with `enabled` (boolean)
  - Renamed `provision_url` → `enrollment_url`; updated description to "In MDM, add `--enrollment_url <enrollment_url>` to the install command" and example URL to `marvisclient://` scheme
  - Updated `createOrgMarvisClientInvite` description to clarify SDK Invites belong to an Org, can be created by an Admin, and can be revoked at anytime
  - Updated request body examples for `createOrgMarvisClientInvite` and `updateOrgMarvisClientInvite`
  - Updated `MarvisClientExample` and `MarvisClientsArrayExample` to include `enrollment_url`

- Updated `GET /api/v1/orgs/{org_id}/jsi/sirt/search`:
  - Updated description to "Search and get all the SIRT for the onboarded devices"
  - Added `updated_after` (string) — JSA Updated date to be filtered after this date
  - Added `updated_before` (string) — JSA Updated date to be filtered before this date
  - Added `published_after` (string) — JSA Published date to be filtered after this date
  - Added `published_before` (string) — JSA Published date to be filtered before this date
  - Added `text` (string) — wildcard search on os_version_affected, affected_models, severity, jsa_id
  - Added `sort` query parameter
  - Updated `severity` description to list valid values (Critical, High, Medium, Low)
  - Updated `id` description to "JSA number"

- Updated `/api/v1/orgs/{org_id}/logs`
  - Renamed path to `/api/v1/orgs/{org_id}/logs/search`
  - Updated description to "Get a list of change logs for the current Org"
- Updated `org_setting_mist_nac` schema:
  - Added `allow_teap_machine_auth_only` (boolean, default: `false`) — allows clients to connect when only Machine Cert succeeds in TEAP authentication
  - Added `mdm` object with `coa_type` field (`"reauth"` (default) or `"disconnect"`) for MDM CoA configuration
- Added `org_setting_mist_nac_mdm` schema

- Updated `org_setting_marvis` schema (Org Setting only):
  - Added `self_driving` object with `wireless`, `wired`, and `wan` sub-objects (each with an `enabled` boolean, default: `false`)
- Added `org_setting_marvis` and `marvis_self_driving` schemas

- Updated `capture_mxedge` schema (Mist Edge Packet Capture):
  - Updated description to "Initiate a Mist Edge Packet Capture"
  - `duration`: added `minimum: 60`, updated `maximum` from `86400` to `10800` (3h)
  - `max_pkt_len`: updated `default` from `128` to `512`, added `minimum: 64`
  - `num_packets`: added `minimum: 0`, updated description to clarify 0 is unlimited for streaming only
  - Added top-level `tcpdump_expression` property (overridden by interface-specific value)
- Updated `response_pcap_search_item` schema:
  - Added `last_seen` (number) property
  - Added `mxedges` (array of strings) property
- Updated `PcapsSearchExample` to include an mxedge capture result
- Updated `response_pcap_status` schema:
  - Added `enabled`, `expiry`, `invalid_mxedges`, `mxedge_count`, `org_id`, `raw`, `site_id`, `timestamp` properties
  - Fixed `max_pkt_len` example from `128` to `512`
- Updated `response_pcap_status_mxedges` schema from array to dict keyed by mxedge_id (with `interfaces`)
- Added `response_pcap_status_mxedges_item` schema
- Added `PcapStatusMxEdgeExample` example
- Updated `startOrgPacketCapture` endpoint description:
  - Fixed WebSocket subscribe channel from `/sites/{site_id}/pcaps` to `/orgs/:org_id/pcaps`
  - Renamed response section from "Wireless/RadioTap" to "MxEdge"
  - Added `lost_messages` field to `pcap_dict` in the response example
  - Added stop response example (when `pcap_dict` is `null`)
- Updated `listOrgMxEdgesStats` endpoint description:
- Added `GET /api/v1/orgs/{org_id}/exports/e911_report` — get E911 AP BSSID report status and download URL
- Added `POST /api/v1/orgs/{org_id}/exports/e911_report` — enable automatic E911 report generation (immediate + every 24h)
- Added `DELETE /api/v1/orgs/{org_id}/exports/e911_report` — disable automatic E911 report generation
- Added `org_e911_report` schema and `OrgE911Report` response component
- Added `POST /api/v1/orgs/{org_id}/nac_clients/{client_mac}/coa`
  - New endpoint to send a CoA (Change of Authorization) command to a NAC client
  - Request: `coa_type` (`reauth` (default) or `disconnect`); Response: `device_type` and `device_mac` of the target device
- Added `nac_client_coa` and `nac_client_coa_response` schemas
- Added `PUT /api/v1/orgs/{org_id}/mxedges/upgrade/{upgrade_id}`
  - New endpoint to update a Mist Edge upgrade job (only `queued` state upgrades can be updated)
- Added `POST /api/v1/orgs/{org_id}/mxedges/upgrade/{upgrade_id}/cancel`
  - New endpoint to cancel a Mist Edge upgrade (best effort; already-upgraded devices are unaffected)
- Added `POST /api/v1/orgs/{org_id}/ssos/{sso_id}/delete_admins`
  - New endpoint to delete SSO admin users by email address
  - Request: `emails` array; Response: `deleted` (succeeded) and `errors` (failed) arrays
- Added `sso_delete_admins` and `sso_delete_admins_response` schemas
- Updated `psk` schema:
  - Added `vlan_name` (string, optional) — VLAN name to assign; `vlan_id` takes precedence if both are provided
- Updated `gateway_port_config` schema:
  - Added `poe_keep_state_when_reboot` (boolean, default: `false`) — controls whether PoE state is preserved across device reboots
- Updated `bgp_config_neighbors` schema:
  - Added `tunnel_via` (enum: `primary` (default), `secondary`) — specifies which tunnel a BGP neighbor is associated with when `via`==`tunnel`
- Updated `installer_device` schema:
  - Added `ble_stat` object with `uuid`, `major`, and `minors` fields
- Added `installer_device_ble_stat` schema
- Updated `account_skyatp_config` schema and `account_skyatp_info` schema:
  - Added `cloud_name` field (enum: `www.amerskyatp.com`, `www.apacskyatp.com`, `www.euroskyatp.com`, `www.canadaskyatp.com`)
- Updated `POST /api/v1/orgs/{org_id}/setting/skyatp/setup` request body example to include `cloud_name`

## [2602.1.10] - 2026-04-08

- Added `minis-application` webhook sample
- Updated `listOrgSecIntelProfiles` to support pagination via `limit` and `page` query parameters

## [2602.1.9] - 2026-03-19

- Updated schema definitions for `gateway` and `gateway_template`:
  - Added `gateway_mgmt` field with sub-properties: `admin_sshkeys`, `app_probing`, `app_usage`, `auto_signature_update`, `config_revert_timer`, `disable_console`, `disable_oob`, `disable_usb`, `fips_enabled`, `probe_hosts`, `probe_hostsv6`, `protect_re`, `root_password`, `security_log_source_address`, `security_log_source_interface`
- Updated schema definitions for `site_setting`:
  - Consolidated `gateway_mgmt` to use shared `#/components/schemas/gateway_mgmt` schema
- Removed deprecated schemas (now consolidated into `gateway_mgmt`):
  - `site_setting_gateway_mgmt`, `site_setting_gateway_mgmt_admin_sshkeys`, `site_setting_gateway_mgmt_auto_signature_update`, `site_setting_gateway_mgmt_probe_hosts`, `site_setting_gateway_mgmt_probe_hostsv6`
- Added `format: password` to sensitive credential fields across multiple schemas for improved security handling (passwords, secrets, API keys, auth tokens)

## [2602.1.8] - 2026-03-18

- Updated `/api/v1/sites/{site_id}/insights/device/{device_mac}/{metric}`
  - Added optional `port_id` query parameter for interface-specific metrics
- Updated `/api/v1/sites/{site_id}/insights/gateway/{device_id}/stats`
  - Added optional `port_id` query parameter for interface-specific metrics
- Updated `/api/v1/sites/{site_id}/insights/mxedge/{device_mac}/{metric}`
  - Added optional `port_id` query parameter for interface-specific metrics
- Updated `/api/v1/sites/{site_id}/insights/switch/{device_mac}/{metric}`
  - Added optional `port_id` query parameter for interface-specific metrics

## [2602.1.7] - 2026-03-18

- Added `/api/v1/sites/{site_id}/insights/ap/{device_id}/stats`
  - New endpoint for AP Insight Metrics with required `metrics` query parameter
- Updated `/api/v1/orgs/{org_id}/stats`
  - Removed `start`, `end`, `duration`, `limit`, `page` query parameters not applicable to org-level stats endpoint
- Updated `/api/v1/orgs/{org_id}/stats/sites`
  - Removed `start`, `end`, `duration` query parameters not applicable to site-level stats endpoint
- Updated `/api/v1/sites/{site_id}/insights`
  - Changed path from `/api/v1/sites/{site_id}/insights/{metric}` to use `metrics` query parameter instead of path parameter
- Updated `/api/v1/sites/{site_id}/insights/client/{client_mac}`
  - Changed path from `/api/v1/sites/{site_id}/insights/client/{client_mac}/{metric}` to use `metrics` query parameter instead of path parameter
- Updated `/api/v1/sites/{site_id}/insights/gateway/{device_id}/stats`
  - Changed path from `/api/v1/sites/{site_id}/insights/gateway/{device_id}/stats/{metric}` to use `metrics` query parameter instead of path parameter
- Updated schema definitions for `gateway` and `gateway_template`:
  - `.oob_ip_configs.vlan_id`, `.oob_ip_configs.node1.vlan_id`: Changed type from `string` to `oneOf` with `string` and `integer` to support both string and numeric VLAN IDs

## [2602.1.6] - 2026-03-05

- Improve query parameter descriptions when partial search is supported with wildcard (`*`) for better clarity on search behavior
- Updated schema definitions
  - Added `uplink` field (boolean) to `stats_switch_port` to indicate if interface is an uplink port

## [2602.1.5] - 2026-03-03

- Updated `/api/v1/sites/{site_id}/insights/fingerprints/count` and `/api/v1/sites/{site_id}/insights/fingerprints/search`
  - Updated operationIds from `countOrgClientFingerprints`/`searchOrgClientFingerprints` to `countSiteClientFingerprints`/`searchSiteClientFingerprints`
  - Updated tag from `Orgs NAC Fingerprints` to `Sites NAC Fingerprints`
- Updated `/api/v1/orgs/{org_id}/inventory`
  - Removed `vc_mac` and `master_mac` query parameters 
  - Added `model` and `name` query parameters
  - Updated `status` parameter to use enum reference (`connected`, `disconnected`)
- Updated `/api/v1/sites/{site_id}/devices/{device_id}/clear_dot1x_mac_limit`
  - Changed `port_id` to `ports` (array) to support clearing multiple ports
- Updated `/api/v1/sites/{site_id}/devices/{device_id}/clear_policy_hit_count`
  - Added `policy_name` request body parameter (required)
- Updated `/api/v1/sites/{site_id}/devices/{device_id}/show_arp`
  - Changed tag from `Utilities Common` to `Utilities LAN`
- Updated schema definitions
  - `clear_dot1x_session`: changed `port_id` to `ports` (array)
  - `utils_clear_bpdu`: changed `port` to `ports` (array)
  - `utils_release_dhcp_leases`: changed `mac` to `macs`
  - `utils_show_arp`: added `node` field for HA cluster support on Gateways

## [2602.1.4] - 2026-02-26

- Updated `/api/v1/orgs/{org_id}/inventory`
  - Updated `type` parameter to support multiple comma-separated values from: `ap`, `gateway`, `router`, `switch`, `all` (default: `ap`)
- Updated `/api/v1/orgs/{org_id}/jsi/inventory/search`
  - Replaced `eol_duration` and `eos_duration` with date-based filters: `eol_after`, `eol_before`, `eos_after`, `eos_before`
  - Added `version_eos_after` and `version_eos_before` parameters for software version end-of-support filtering
  - Added `sirt_id` and `pbn_id` parameters for security advisory filtering
  - Updated `text` parameter description to clarify wildcard support
- Updated `/api/v1/sites/{site_id}/devices`
  - Updated `type` parameter to support multiple comma-separated values from: `ap`, `gateway`, `router`, `switch`, `all` (default: `ap`)
- Added `/api/v1/sites/{site_id}/mapstacks`
- Updated `/api/v1/sites/{site_id}/setting`
  - Added `gateway_tunnel_updown_threshold` field (integer) to enable threshold-based gateway tunnel (secure edge tunnels) up-down delivery
  - Added `allow_mist` field (boolean) to control whether Mist can access this site
  - Added `ap_synthetic_test.additional_vlan_ids` field (array of integers) for additional VLAN IDs in synthetic tests
- Updated webhook schemas
  - Added new webhook topic `minis-reachability` for AP synthetic test reachability events
  - Updated `webhook_minis_reachability_event` timestamp field to use shared `#/components/schemas/timestamp` reference for consistency
  - Added webhook sample endpoint for `minis-reachability` topic at `/webhooks/minis_reachability`
- Updated schema definitions
  - Added `wlan.disable_message_authenticator_check` field (boolean) to disable Message-Authenticator Check for RADIUS message integrity verification (default: false for better security)
  - Updated `extra_route` and `extra_route6` schemas to reference shared `next_hop_via` schema for better reusability and support for ECMP (Equal-Cost Multi-Path) load balancing
  - Replaced `mapstack_id` and `mapstack_floor` with `group_name` and `group_idx` in map schema for maps grouping (group_idx typically used for floor)

## [2602.1.3] - 2026-02-24

- Updated websocket API examples for clarity and completeness
- Improved `alarm_group` description
- Added missing `site_id` query parameter to `searchOrgWanClients`
- Added missing query parameter `message` and `sort` to `listSelfAuditLogs`

## [2602.1.2] - 2026-02-24

- Updated `/api/v1/sites/{site_id}`
  - Added `routertemplate_id` field
- Updated `/api/v1/orgs/{org_id}/sites`
  - Added `routertemplate_id` field

## [2602.1.1] - 2026-02-19

- Updated `/api/v1/orgs/{org_id}/sites/search`
  - Updated `name` parameter description to clarify it is case insensitive and supports partial search with wildcard (`*`)
- Updated `/api/v1/orgs/{org_id}/stats/ports/search`
  - Removed unsupported `site_id` query parameter
- Updated schema definitions
  - Added `deprecated: true` attribute to `managed` and `disable_auto_config` fields
  - Fixed inline complex definitions

## [2602.1.0] - 2026-02-10

- Added `/api/v1/orgs/{org_id}/aos/register_cmd`
- Added `/api/v1/orgs/{org_id}/jsi/pbn/count`
- Added `/api/v1/orgs/{org_id}/jsi/pbn/search`
- Added `/api/v1/orgs/{org_id}/jsi/sirt/count`
- Added `/api/v1/orgs/{org_id}/jsi/sirt/search`
- Added `/api/v1/orgs/{org_id}/mxedges/{mxedge_id}/vm_params`
- Added `/api/v1/orgs/{org_id}/usermacs/count`
- Added `/api/v1/sites/{site_id}/maps/auto_geofences`
  - Run auto geofence service for all maps in a site
- Added `/api/v1/sites/{site_id}/maps/{map_id}/auto_geofences`
  - Run auto geofence service for a single map
- Updated `/api/v1/orgs/{org_id}/nac_clients/search`
- Updated `/api/v1/orgs/{org_id}/setting`
  - Added `allow_mist` field
- Updated `/api/v1/orgs/{org_id}/stats`
  - Added `allow_mist` field to response
- Updated `/api/v1/sites/{site_id}/analyze_spectrum`
  - Added `channels` parameter to request body
  - Added `minimum: 60` constraint to `duration` parameter
- Updated `/api/v1/sites/{site_id}/setting/derived`
  - Added `allow_mist` field to response
- Updated `/api/v1/sites/{site_id}/stats/devices`
  - Added `ip`, `mac`, `product_id`, `vendor_id` fields to `esl_stat` for Hanshow and SoluM dongles

## [2511.1.6] - 2025-12-11

- Updated `/api/v1/orgs/{org_id}/networktemplates`
  Updated `/api/v1/orgs/{org_id}/networktemplates/{networktemplate_id}`
  Updated `/api/v1/sites/{site_id}/devices`
  Updated `/api/v1/sites/{site_id}/devices/import`
  Updated `/api/v1/sites/{site_id}/devices/{device_id}`
  Updated `/api/v1/sites/{site_id}/networktemplates/derived`
  Updated `/api/v1/sites/{site_id}/setting`
  Updated `/api/v1/sites/{site_id}/setting/derived`
  - Added `bgp_config` for switches
- Updated `/api/v1/orgs/{org_id}/deviceprofiles`
  Updated `/api/v1/orgs/{org_id}/deviceprofiles/{deviceprofile_id}`
  Updated `/api/v1/orgs/{org_id}/evpn_topologies`
  Updated `/api/v1/orgs/{org_id}/evpn_topologies/{evpn_topology_id}`
  Updated `/api/v1/orgs/{org_id}/networktemplates`
  Updated `/api/v1/orgs/{org_id}/networktemplates/{networktemplate_id}`
  Updated `/api/v1/sites/{site_id}/deviceprofiles/derived`
  Updated `/api/v1/sites/{site_id}/devices`
  Updated `/api/v1/sites/{site_id}/devices/import`
  Updated `/api/v1/sites/{site_id}/devices/{device_id}`
  Updated `/api/v1/sites/{site_id}/evpn_topologies`
  Updated `/api/v1/sites/{site_id}/evpn_topologies/{evpn_topology_id}`
  Updated `/api/v1/sites/{site_id}/networktemplates/derived`
  Updated `/api/v1/sites/{site_id}/setting`
  Updated `/api/v1/sites/{site_id}/setting/derived`
  - Added `networks` to `port_config`
- Updated `/api/v1/orgs/{org_id}/deviceprofiles`
  Updated `/api/v1/orgs/{org_id}/deviceprofiles/{deviceprofile_id}`
  Updated `/api/v1/orgs/{org_id}/gatewaytemplates`
  Updated `/api/v1/orgs/{org_id}/gatewaytemplates/{gatewaytemplate_id}`
  Updated `/api/v1/sites/{site_id}/deviceprofiles/derived`
  Updated `/api/v1/sites/{site_id}/gatewaytemplates/derived`
  Updated `/api/v1/sites/{site_id}/setting`
  Updated `/api/v1/sites/{site_id}/setting/derived`
  - Updated `gateway_matching` to use `gateway_port_config` component for `port_config` property


## [2511.1.0] - 2025-11-17

- Marked `/api/v1/orgs/{org_id}/128routers/register_cmd` as deprecated, replaced by `/api/v1/orgs/{org_id}/ssr/register_cmd`
- Added `/api/v1/orgs/{org_id}/ssr/export_idtokens`
- Added `/api/v1/orgs/{org_id}/stats/ospf_peers/count`
- Added `/api/v1/orgs/{org_id}/stats/ospf_peers/search`
- Added `/api/v1/sites/{site_id}/devices/gbp_tag`
- Added `/api/v1/sites/{site_id}/stats/ospf_peers/count`
- Added `/api/v1/sites/{site_id}/stats/ospf_peers/search`
- Updated `/api/v1/orgs/{org_id}/devices/last_config/search`
  - Added `cert_expiry_duration` query parameter
- Updated `/api/v1/orgs/{org_id}/deviceprofiles`
  - Renamed `ant_mode` to `antenna_select`, added `rrm_managed`, `antenna_beam_pattern`
  - Added `skyatp` and `syslog` to gateway `service_policies`
  - Added `bypass_auth_when_server_down_for_voip` and `poe_priority` for switch ports
- Updated `/api/v1/orgs/{org_id}/deviceprofiles/{deviceprofile_id}`
  - Renamed `ant_mode` to `antenna_select`, added `rrm_managed`, `antenna_beam_pattern`
  - Added `skyatp` and `syslog` to gateway `service_policies`
  - Added `bypass_auth_when_server_down_for_voip` and `poe_priority` for switch ports
- Updated `/api/v1/orgs/{org_id}/evpn_topologies`
  - Added `bypass_auth_when_server_down_for_voip` and `poe_priority` for switch ports
- Updated `/api/v1/orgs/{org_id}/evpn_topologies/{evpn_topology_id}`
  - Added `bypass_auth_when_server_down_for_voip` and `poe_priority` for switch ports
- Updated `/api/v1/orgs/{org_id}/gatewaytemplates`
  - Added `skyatp` and `syslog` to gateway `service_policies`
- Updated `/api/v1/orgs/{org_id}/gatewaytemplates/{gatewaytemplate_id}`
  - Added `skyatp` and `syslog` to gateway `service_policies`
- Updated `/api/v1/orgs/{org_id}/jsi/inventory/search`
  - Added `claimed` query parameter
  - Added `has_support` query parameter
- Updated `/api/v1/orgs/{org_id}/mxclusters`
  - Added `disabled` to `proxy`
- Updated `/api/v1/orgs/{org_id}/mxclusters/{mxcluster_id}`
  - Added `disabled` to `proxy`
- Updated `/api/v1/orgs/{org_id}/mxedges`
  - Added `disabled` to `proxy`
- Updated `/api/v1/orgs/{org_id}/mxedges/{mxedge_id}`
  - Added `disabled` to `proxy`
- Updated `/api/v1/orgs/{org_id}/mxedges/search`
  - Added `inactive_vlan_strs`
- Updated `/api/v1/orgs/{org_id}/nacportals`
  - Added `additional_cacerts`
- Updated `/api/v1/orgs/{org_id}/nacportals/{nacportal_id}`
  - Added `additional_cacerts`
- Updated `/api/v1/orgs/{org_id}/networktemplates`
  - Added `bypass_auth_when_server_down_for_voip` and `poe_priority` for ports
- Updated `/api/v1/orgs/{org_id}/networktemplates/{networktemplate_id}`
  - Added `bypass_auth_when_server_down_for_voip` and `poe_priority` for ports
- Updated `/api/v1/orgs/{org_id}/setting`
  - Added `disabled` to ssr `proxy`
- Updated `/api/v1/orgs/{org_id}/sites`
  - Removed `apporttemplate_id` from response
- Updated `/api/v1/orgs/{org_id}/stats/devices`
  - Added `poe_priority` for switch stats
- Updated `/api/v1/orgs/{org_id}/stats/mxedges`
  - Added `inactive_vlan_strs`
- Updated `/api/v1/orgs/{org_id}/stats/mxedges/{mxedge_id}`
  - Added `inactive_vlan_strs`
- Updated `/api/v1/orgs/{org_id}/stats/ports/search`
  - Added `poe_priority` query parameter
- Updated `/api/v1/installer/orgs/{org_id}/sites/{site_name}/maps`
  - Added `group_idx` and `group_name` to response
- Updated `/api/v1/installer/orgs/{org_id}/sites/{site_name}/maps/{map_id}`
  - Added `group_idx` and `group_name` to request and response
- Updated `/api/v1/sites/{site_id}`
  - Removed `apporttemplate_id` from response
- Updated `/api/v1/sites/{site_id}/devices`
  - Renamed `ant_mode` to `antenna_select`, added `rrm_managed`, `antenna_beam_pattern`
  - Added `skyatp` and `syslog` to gateway `service_policies`
  - Added `bypass_auth_when_server_down_for_voip` and `poe_priority` for switch ports
- Updated `/api/v1/sites/{site_id}/devices/clear_pending_version`
  - Added request body schema and example
- Updated `/api/v1/sites/{site_id}/devices/import`
  - Renamed `ant_mode` to `antenna_select`, added `rrm_managed`, `antenna_beam_pattern`
  - Added `skyatp` and `syslog` to gateway `service_policies`
  - Added `bypass_auth_when_server_down_for_voip` and `poe_priority` for switch ports
- Updated `/api/v1/sites/{site_id}/devices/last_config/search`
  - Added `cert_expiry_duration` query parameter
- Updated `/api/v1/sites/{site_id}/devices/restore_backup_version`
  - Added request body schema and example
  - Updated supported devices listed in description
- Updated `/api/v1/sites/{site_id}/devices/{device_id}`
  - Renamed `ant_mode` to `antenna_select`, added `rrm_managed`, `antenna_beam_pattern`
  - Added `skyatp` and `syslog` to gateway `service_policies`
  - Added `bypass_auth_when_server_down_for_voip` and `poe_priority` for switch ports
- Updated `/api/v1/sites/{site_id}/devices/{device_id}/ping`
  - Added `vrf`
- Updated `/api/v1/sites/{site_id}/devices/{device_id}/restore_backup_version`
  - Updated supported devices listed in description
- Updated `/api/v1/sites/{site_id}/deviceprofiles/derived`
  - Renamed `ant_mode` to `antenna_select`, added `rrm_managed`, `antenna_beam_pattern`
  - Added `skyatp` and `syslog` to gateway `service_policies`
  - Added `bypass_auth_when_server_down_for_voip` and `poe_priority` for switch ports
- Updated `/api/v1/sites/{site_id}/evpn_topologies`
  - Added `bypass_auth_when_server_down_for_voip` and `poe_priority` for switch ports
- Updated `/api/v1/sites/{site_id}/evpn_topologies/{evpn_topology_id}`
  - Added `bypass_auth_when_server_down_for_voip` and `poe_priority` for switch ports
- Updated `/api/v1/sites/{site_id}/maps`
  - Added `group_idx` and `group_name` to request and response
- Updated `/api/v1/sites/{site_id}/maps/{map_id}`
  - Added `group_idx` and `group_name` to request and response
- Updated `/api/v1/sites/{site_id}/mxedges`
  - Added `disabled` to `proxy`
- Updated `/api/v1/sites/{site_id}/mxedges/{mxedge_id}`
  - Added `disabled` to `proxy`
- Updated `/api/v1/sites/{site_id}/networktemplates/derived`
  - Added `bypass_auth_when_server_down_for_voip` and `poe_priority` for ports
- Updated `/api/v1/sites/{site_id}/setting`
  - Renamed `ant_mode` to `antenna_select`, added `rrm_managed`, `antenna_beam_pattern`
  - Added `disabled` to `proxy`
  - Added `skyatp` and `syslog` to gateway `service_policies`
  - Added `disabled` to ssr `proxy`
  - Added `bypass_auth_when_server_down_for_voip` and `poe_priority` for switches and ports
- Updated `/api/v1/sites/{site_id}/setting/derived`
  - Renamed `ant_mode` to `antenna_select`, added `rrm_managed`, `antenna_beam_pattern`
  - Added `disabled` to `proxy`
  - Added `skyatp` and `syslog` to gateway `service_policies`
  - Added `disabled` to ssr `proxy`
  - Added `bypass_auth_when_server_down_for_voip` and `poe_priority` for switches and ports
- Updated `/api/v1/sites/{site_id}/stats/devices`
  - Renamed `ant_mode` to `antenna_select`
  - Added `poe_priority` for switch stats
- Updated `/api/v1/sites/{site_id}/stats/devices/{device_id}`
  - Renamed `ant_mode` to `antenna_select`
  - Added `poe_priority` for switch stats
- Updated `/api/v1/sites/{site_id}/stats/mxedges`
  - Added `inactive_vlan_strs`
- Updated `/api/v1/sites/{site_id}/stats/mxedges/{mxedge_id}`
  - Added `inactive_vlan_strs`
- Updated `/api/v1/sites/{site_id}/stats/ports/search`
  - Added `poe_priority`
  