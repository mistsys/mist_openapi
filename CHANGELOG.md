# Changelog

All notable changes to this project will be documented in this file.

## [2606.1.1] - 2026-07-10
- Fixed `site_setting` schema: renamed attribute `mxtunnels` to `mxtunnel`

## [2606.1.0] - 2026-06-24

- Updated `evpn_topology_switch_role` schema:
  - Added `border` role
- Updated `mxedge` schema:
  - Updated `mxcluster_id` to accept `null`

## [2605.1.2] - 2026-06-22

- Added `id` and `org_id` fields to the `nac_portal` schema to directly expose Organization ID and Portal ID in API responses (previously only available through `additional_properties` in SDK)

## [2605.1.1] - 2026-06-15

- Fixed `power` field validation in AP and RF template radio band schemas (`ap_radio_band24`, `ap_radio_band5`, `ap_radio_band6`, `rftemplate_radio_band24`, `rftemplate_radio_band5`, `rftemplate_radio_band6`): corrected `minimum` from 3 (2.4 GHz) / 5 (5 GHz, 6 GHz) to 0 to match actual API behavior; updated description to clarify the field is in dBm with range 0–25 for static power or `null`/unset for auto power mode
- Fixed `power_max` default and maximum in `rftemplate_radio_band6` from 18 to 17

## [2605.1.0] - 2026-06-08

- `GET /api/v1/orgs/{org_id}/inventory`: Added `disconnected_before` query parameter to filter devices that were last disconnected before a given epoch timestamp
- Added `last_disconnected` field (integer, epoch seconds) to the `inventory` schema and `OrgInventoryExample`
- `POST /api/v1/orgs/{org_id}/claim`: Updated description to clarify the endpoint is synchronous — all inventory devices are claimed immediately during the request; removed `async` request body parameter
- Updated `device_type` field description in `claim_activation` request schema to clarify it limits the claim to a specific device type
- Added `POST /api/v1/orgs/{org_id}/claims`: new async claim endpoint that queues inventory claiming in the background and returns immediately with a `claim_id`; licenses (if `type=all`) are still claimed synchronously
- Added `GET /api/v1/orgs/{org_id}/claims`: list all async inventory claim jobs for the organization, with optional `detail` parameter for per-device results
- Added `GET /api/v1/orgs/{org_id}/claims/{claim_id}`: poll the status of a specific async claim job
- `GET /api/v1/orgs/{org_id}/setting`: Added `src_ips` field to `org_setting_api_policy` schema — optional list of allowed source IP addresses/CIDR subnets (max 10) for org API access
- `GET /api/v1/orgs/{org_id}/setting`: Added `disable_proactive_monitoring` field to `org_setting_marvis` schema
- `POST /api/v1/orgs/{org_id}/ssos`: Replaced the nested `openroaming` object with three flat top-level fields: `openroaming_ssids`, `openroaming_wba_client_cert`, and `openroaming_wba_client_key`; marked the `sso_openroaming` schema and its `wba_cert` field as deprecated
- `GET /api/v1/orgs/{org_id}/mxclusters`: Added `mist_nacedge` field to `mxcluster` schema — NAC Edge survivability settings (new `mxcluster_nacedge` schema) with fields `enabled`, `caching_site_ids`, `nac_edge_hosts`, `auth_ttl`, `default_vlan`, and `default_dot1x_vlan`; requires `mist_nac` to be enabled on the cluster
- `GET /api/v1/orgs/{org_id}/nactags`: Added path-level description explaining NAC Tags as building blocks for NAC Rules, including classifier vs. result-attribute roles, multi-value OR/AND matching via `match_all`, wildcard operators (`*` prefix, suffix, substring), negation (`!`), and `regex=` prefix for full regular-expression matching
- `GET /api/v1/orgs/{org_id}/jsi/inventory/search`: Renamed query parameters `eol_after`/`eol_before` to `end_of_sale_after`/`end_of_sale_before`; renamed `eol_time` to `end_of_sale_time` in response schema, `jsi_inventory_count_distinct` enum, and examples; added 18 new customer/contract fields to `js_inventory_item` returned only for onboarded (claimed) devices: `availability`, `contract_end_date`, `contract_reseller`, `contract_start_date`, `contract_type`, `current_contract_flag`, `distributor`, `ia_address`, `ia_country`, `ia_region`, `ia_zip_postal`, `service_contract_no`, `service_contract_type`, `service_decline_flag`, `service_eligible`, `ship_date_calc`, `warranty_end`, `warranty_start`
- `PUT /api/v1/orgs/{org_id}/usermacs`: Request body now accepts two forms — an array of user MAC objects (asynchronous, `id` required per entry) or a dict with `consistency` and `usermacs` fields (new `user_macs_update_body` schema); `consistency`==`strong` makes the call synchronous and returns `updated`/`errors` lists, `eventual` (default) returns immediately with `{"detail": "batch update in progress"}`; added `detail` field to `user_macs_update` response schema; added `UserMacsUpdateAsyncExample`
- `POST /api/v1/orgs/{org_id}/usermacs/import`: JSON body now accepts array form (async by default) or dict form with explicit `consistency` control (reuses `user_macs_update_body` schema); CSV multipart upload now accepts optional `consistency` field alongside `file`; added `detail` field to `user_mac_import` response schema; added `UserMacImportAsyncExample`
- Added `GET /api/v1/orgs/{org_id}/stats/marvisclients/search`: new endpoint to search Marvis Client stats records with filters (`device_id`, `wifi_mac`, `wifi_ip`, `hostname`, `model`, `mfg`, `serial`, `os_type`, `os_version`) and pagination; returns `stats_marvis_clients_search` schema (new)
- Added `GET /api/v1/orgs/{org_id}/stats/marvisclients/count`: new endpoint to count Marvis Client stats records by a distinct field (default `os_type`); returns standard `response_count`
- Added `GET /api/v1/orgs/{org_id}/marvisclients/events/search`: new endpoint to search Marvis Client events with filters (`type`, `device_id`, `wifi_mac`, `wifi_ip`, `hostname`, `ssid`, `bssid`, `channel`, `pre_bssid`, `pre_channel`); returns `marvis_client_events_search` schema (new)
- Added `GET /api/v1/orgs/{org_id}/marvisclients/events/count`: new endpoint to count Marvis Client events by a distinct field (default `type`); returns standard `response_count`
- Added `GET /api/v1/orgs/{org_id}/insights/marvisclient/{marvisclient_id}/marvisclient-metrics`: new endpoint to retrieve time-series performance metrics (Wi-Fi RSSI, cellular RSSI, battery, CPU, memory) for a specific Marvis Client device; returns `marvis_client_insights` schema (new)
- New schemas: `marvis_client_event`, `marvis_client_event_neighbor_ap`, `marvis_client_events_search`, `marvis_client_insights`, `stats_marvis_client`, `stats_marvis_client_location`, `stats_marvis_clients_search`
- `GET /api/v1/orgs/{org_id}/setting/mist_scep/client_certs`: replaced `sso_name_id` query param with `common_name` and `cert_provider`; added `expire_time` and `created_time` filter params; added `limit` and `page` pagination params; changed `created_time` and `expire_time` fields in `issued_client_certificate` schema from datetime strings to integer epoch seconds; added `limit` and `page` fields to `issued_client_certificates_results` schema; updated example
- `POST /api/v1/sites/{site_id}/wlans` (and WLAN schema): added `enable_ftm` field (boolean, default `false`) to enable FTM (Fine-Time Measurement, 802.11mc), configuring the AP as an FTM Responder (target) to allow clients to perform ranging requests against it; added `smsglobal_sender` field (string, optional) to `wlan_portal` schema for sender's number or sender ID
- `POST /api/v1/utils/test_smsglobal`: added optional `smsglobal_sender` field to request body and example
- `GET /api/v1/sites/{site_id}/maps`: added optional `mapstack_id` query parameter (UUID) to filter maps by mapstack
- `PUT /api/v1/sites/{site_id}/devices/{device_id}` (and AP schemas): added `mqtt_config` field to `device_ap` and `deviceprofile_ap` schemas; new `ap_mqtt` schema with fields `enabled`, `broker_host`, `broker_port`, `broker_proto` (`tcp`/`ssl`), `username`, `password`, `format` (`raw`/`json`); BLE advertisements are forwarded per AssetFilter `mqtt_topic`
- `PUT /api/v1/sites/{site_id}/devices/{device_id}` (`junos_port_config` schema): added `ae_lacp_passive` field (boolean, default `false`); when `true`, sets LACP to passive mode on the AE interface
- `PUT /api/v1/sites/{site_id}/setting` (`switch_port_usage` schema): added `server_fail_retry_interval` field (integer, default `120`, range 120-65535); only applicable when `port_auth`==`dot1x`; sets the interval in seconds to retry authentication after a RADIUS server failure
- `POST /api/v1/sites/{site_id}/assetfilters` (and `asset_filter` schema): added optional `mqtt_topic` field (string); if set, matching BLE advertisements are forwarded to this MQTT topic when MQTT publishing is enabled
- `GET /api/v1/sites/{site_id}/stats/assets`: added optional `map_id` query parameter (UUID) to filter assets by map; added `battery_percent` field (integer, 1–100%) to `stats_asset` schema for Aruba/HPE asset tags
- `PUT /api/v1/sites/{site_id}/setting` (`iotproxy_visionline` schema): added `cacerts` field (array of strings); PEM-encoded CA certificates required to verify the Visionline collector's TLS certificate when it uses a self-signed certificate
- `PUT /api/v1/sites/{site_id}/setting` (`mist_nacedge` schema): added `caching_site_ids` field (array of UUIDs); list of site UUIDs whose auth requests should be cached by NAC Edges assigned to this site
- Added `GET /api/v1/sites/{site_id}/marvis_configs/search`: search Marvis Config Actions with filters (`mac`, `type`, `src`, `admin_id`, `op`, `port_id`, `vlan_ids`, `reason`); returns paginated `marvis_config_actions_search` (new)
- Added `GET /api/v1/sites/{site_id}/marvis_configs/count`: count Marvis Config Actions by a distinct field (default `mac`); returns standard `response_count`
- Added `DELETE /api/v1/sites/{site_id}/marvis_configs/{id}`: delete a Marvis-injected config action
- Added `POST /api/v1/sites/{site_id}/marvis_configs/{id}/feedback`: submit feedback on a Marvis config action (e.g. mark as `invalid`); request body and response use new `marvis_config_feedback` / `marvis_config_feedback_response` schemas
- `GET /api/v1/sites/{site_id}/analyze_spectrum` (`response_running_spectrum_analysis` schema): added `width` (integer, channel width in MHz) and `channels` (array of integers, scanned channel numbers)
- `POST /api/v1/sites/{site_id}/analyze_spectrum` (`spectrum_analysis` schema): fixed `channels` items type from `string` to `integer`
- Added `POST /api/v1/sites/{site_id}/maps/{map_id}/apply_autoplacement`: accept cached autoplacement/auto-orientation values for a map or subset of APs; request body uses new `autoplacement_localization_selector` schema (`for`: `placement`/`orientation`, `macs`: optional list)
- Updated `POST /api/v1/sites/{site_id}/maps/{map_id}/clear_autoplacement`: updated description and changed request body from `mac_addresses` to `autoplacement_localization_selector` schema (adds `for` field)
- `POST /api/v1/sites/{site_id}/maps/{map_id}/use_auto_ap_values`: marked as deprecated; replaced by `apply_autoplacement` (accept) and `clear_autoplacement` (reject)

## [2604.1.5] - 2026-06-03
- Improved operations descriptions for better clarity and developer/LLM guidance, including more details on supported features, behavior, and use cases for various endpoints.

## [2604.1.4] - 2026-06-01

- Improved query parameter descriptions across many endpoints: added enum values, clarified `distinct` grouping fields, and standardized filter descriptions for device, client, NAC, inventory, and event search/count operations
- Clarified authentication documentation: API Token is the preferred method for automation, Basic Auth was removed from the documented authentication schemes because it is deprecated and planned for removal in September 2026, and the login session flow uses the `X-CSRFToken` header after `/api/v1/login`
  - Marked public login and account flow endpoints as unauthenticated where appropriate:
    - `POST /api/v1/login`
    - `POST /api/v1/login/lookup`
    - `GET /api/v1/login/oauth/{provider}`
    - `POST /api/v1/login/oauth/{provider}`
    - `POST /api/v1/login/two_factor`
    - `POST /api/v1/invite/verify/{token}`
    - `POST /api/v1/recover`
    - `POST /api/v1/recover/verify/{token}`
    - `POST /api/v1/register`
    - `GET /api/v1/register/recaptcha`
    - `POST /api/v1/register/verify/{token}`
- Updated query parameters:
  - Removed invalid `timestamp` query parameter from:
    - `GET /api/v1/orgs/{org_id}/devices/events/count`
    - `GET /api/v1/orgs/{org_id}/devices/events/search`
    - `GET /api/v1/orgs/{org_id}/nac_clients/count`
    - `GET /api/v1/orgs/{org_id}/nac_clients/events/search`
    - `GET /api/v1/orgs/{org_id}/nac_clients/search`
    - `GET /api/v1/sites/{site_id}/devices/events/search`
    - `GET /api/v1/sites/{site_id}/nac_clients/count`
    - `GET /api/v1/sites/{site_id}/nac_clients/events/search`
    - `GET /api/v1/sites/{site_id}/nac_clients/search`
    - `GET /api/v1/sites/{site_id}/services/events/count`
    - `GET /api/v1/sites/{site_id}/services/events/search`
  - Updated query parameter schemas for comma-separated filter support:
    - `GET /api/v1/orgs/{org_id}/alarms/search`: `site_id`, `group`, `severity`
    - `GET /api/v1/orgs/{org_id}/clients/events/search`: `type`, `reason_code`, `key_mgmt`, `proto`, `band`
    - `GET /api/v1/orgs/{org_id}/clients/sessions/search`: `band`
    - `GET /api/v1/orgs/{org_id}/inventory`: `type`
    - `GET /api/v1/orgs/{org_id}/inventory/search`: `site_id`, `status`
    - `GET /api/v1/orgs/{org_id}/logs`: `site_id`
    - `GET /api/v1/orgs/{org_id}/logs/search`: `site_id`
    - `GET /api/v1/orgs/{org_id}/nactags`: `type`, `match`
    - `GET /api/v1/orgs/{org_id}/stats/devices`: `type`, `status`
    - `GET /api/v1/orgs/{org_id}/stats/ports/search`: `device_type`
    - `GET /api/v1/orgs/{org_id}/stats/vpn_peers/search`: `type`
    - `GET /api/v1/orgs/{org_id}/wired_clients/search`: `source`, `vlan`, `ip`

## [2604.1.3] - 2026-05-29

- Improved numerous schema and response descriptions for clarity and better developer/LLM guidance (OSPF, RADIUS, RadSec, PSK, WLAN, WxLAN, webhooks, stats, NAC, Mist Edge, gateway, and more)

## [2604.1.2] - 2026-05-28

- Improved numerous endpoint and schema descriptions for clarity and better developer/LLM guidance
- Updated schema definitions
  - Marked `device_event.ap` and `device_event.ap_name` as deprecated; use `mac` and `device_name` instead
  - Added `format: password` to the PPPoE `poser_password` field
  - Added `format: password` to the read-only Cradlepoint `cp_api_key` and `ecm_api_key` fields

## [2604.1.0] - 2026-05-05

- Added `GET /api/v1/sites/{site_id}/rrm/channel_scores/band/{band}`
- Added `GET /api/v1/sites/{site_id}/auto_map_assignment`
  Added `POST /api/v1/sites/{site_id}/auto_map_assignment`
  Added `DELETE /api/v1/sites/{site_id}/auto_map_assignment`
  Added `POST /api/v1/sites/{site_id}/apply_auto_map_assignment`
  Added `POST /api/v1/sites/{site_id}/clear_auto_map_assignment`
- Added `POST /api/v1/sites/{site_id}/mxedges/upgrade`
  Added `GET /api/v1/sites/{site_id}/mxedges/upgrade`
  Added `GET /api/v1/sites/{site_id}/mxedges/upgrade/{upgrade_id}`
  Added `PUT /api/v1/sites/{site_id}/mxedges/upgrade/{upgrade_id}`
  Added `POST /api/v1/sites/{site_id}/mxedges/upgrade/{upgrade_id}/cancel`
- Added `POST /api/v1/sites/{site_id}/nac_clients/{client_mac}/coa`
- Added `POST /api/v1/sites/{site_id}/devices/{device_id}/zigbee_join`
- Added `GET /api/v1/sites/{site_id}/iotendpoints/search`
- Added `GET /api/v1/orgs/{org_id}/exports/e911_report`
  Added `POST /api/v1/orgs/{org_id}/exports/e911_report`
  Added `DELETE /api/v1/orgs/{org_id}/exports/e911_report`
- Added `PUT /api/v1/orgs/{org_id}/mxedges/upgrade/{upgrade_id}`
  Added `POST /api/v1/orgs/{org_id}/mxedges/upgrade/{upgrade_id}/cancel`
- Added `POST /api/v1/orgs/{org_id}/nac_clients/{client_mac}/coa`
- Added `POST /api/v1/orgs/{org_id}/ssos/{sso_id}/delete_admins`
- Added `POST /api/v1/msps/{msp_id}/ssos/{sso_id}/delete_admins`
- Updated `/api/v1/orgs/{org_id}/logs`:
  - Renamed to `/api/v1/orgs/{org_id}/logs/search`
- Updated `GET /api/v1/orgs/{org_id}/jsi/sirt/search`:
  - Added `updated_after`, `updated_before`, `published_after`, `published_before`, `text`, `sort` query parameters
- Updated `evpn_config_role` schema:
  - Added `border` role
- Updated `junos_port_config` schema:
  - Added `ae_lacp_force_up`
- Updated `account_skyatp_config`
  Updated `account_skyatp_info`:
  - Added `cloud_name`
- Updated `ap_mesh` schema:
  - Added `use_wpa3_on_5`
- Updated `bgp_config_neighbors` schema:
  - Added `tunnel_via`
- Updated `capture_mxedge` schema:
  - Added `tcpdump_expression`
  - Updated `duration`, `max_pkt_len`, `num_packets` constraints
- Updated `device_ap`
  Updated `deviceprofile_ap`:
  - Added `zigbee_config`
- Updated `evpn_options` schema:
  - Added `enable_inband_mgmt`
- Updated `gateway_port_config` schema:
  - Added `poe_keep_state_when_reboot`
- Updated `installer_device` schema:
  - Added `ble_stat`
- Updated `marvis_client` schema:
  - Added `telemetry`, `location`, `synthetic_test`
  - Renamed `provision_url` → `enrollment_url`
- Updated `org_setting_marvis` schema:
  - Added `self_driving`
- Updated `org_setting_mist_nac` schema:
  - Added `allow_teap_machine_auth_only` and `mdm`
- Updated `psk` schema:
  - Added `vlan_name`
- Updated `response_pcap_search_item` schema:
  - Added `last_seen` and `mxedges`
- Updated `response_pcap_status` schema:
  - Added `enabled`, `expiry`, `invalid_mxedges`, `mxedge_count`, `org_id`, `raw`, `site_id`, `timestamp`
  - Updated `mxedges` from array to dict keyed by `mxedge_id`
- Updated `rrm_event` schema:
  - Renamed `ap_id` → `ap`
- Updated `site_setting` schema:
  - Added `iotproxy` and `vars_annotations`
- Updated `stats_asset` schema:
  - Added `_ttl`, `by`, `device_id`, `id`, `manufacture`, `mfg_company_id`, `mfg_data`, `service_packets`
- Updated `switch_port_config_overwrite`
  Updated `switch_port_usage`:
  - Added `poe_keep_state_when_reboot`
- Updated `utils_clear_bgp`, `utils_ping`, `utils_show_forwarding_table`, `utils_show_route`, `utils_traceroute` descriptions
- Updated `virtual_chassis_update` schema:
  - Added `remove_inventory`
- Updated `wlan_auth` schema:
  - Added `enable_gcmp256` and `enable_beacon_protection`
- Updated `GET /api/v1/orgs/{org_id}/inventory/count`:
  - Added `site_id` query parameter
  - Added `model` query parameter
  - Added `version` query parameter
  - Added `status` query parameter

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
