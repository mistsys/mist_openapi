# Changelog

All notable changes to this project will be documented in this file.

## [2611.1.0] - 2026-11-15

- Added `POST /api/v1/orgs/{org_id}/inventory/update_model` (set the intended model, and resulting device type, of common hardware before the device onboards; per-MAC `success`/`error`/`reason` response); added `inventory_update_model`, `inventory_update_models` and `response_inventory_update_model` schemas, and the `OrgInventoryUpdateModel` response
- Added the OAuth2 authorization code flow (with PKCE and rotating refresh tokens) for API tokens with `oauth_enabled`: `GET/POST /api/v1/orgs/oauth/authorize` and `POST /api/v1/orgs/oauth/token` (`authorization_code` and `refresh_token` grants); added `oauth_authorize_grant`, `oauth_authorize_info`, `oauth_login_required`, `oauth_token_request`, `oauth_token_request_authorization_code`, `oauth_token_request_refresh_token` and `oauth_token_response` schemas, the `OauthAuthorizeInfo`, `OauthAuthorizeRedirect`, `OauthLoginRequired` and `OauthToken` responses, and the `Orgs OAuth2` tag
- `POST /api/v1/orgs/{org_id}/apitokens`, `GET /api/v1/orgs/{org_id}/apitokens`, `GET/PUT /api/v1/orgs/{org_id}/apitokens/{apitoken_id}` (`org_apitoken` schema): added OAuth2 client settings `oauth_enabled`, `oauth_ttl` (default 3600, max 86400), `oauth_redirect_uris`, `oauth_pkce_required` and read-only `oauth_client_id` (`<org_id>.<token_id>`, present when `oauth_enabled`==`true`); `src_ips` can now be updated with `PUT`
- `GET /api/v1/orgs/{org_id}/logs/search` (`audit_log` schema): added read-only `acting_admin_id` (present only for actions performed via an OAuth access token: the user who consented to the OAuth application, while `admin_id`/`admin_name` identify the OAuth token)
- `GET /api/v1/orgs/{org_id}/logs/search` and `GET /api/v1/orgs/{org_id}/logs/count`: added `category` (`audit_log` schema property present only for config changes, `category` filter on search where `*` matches any categorized change, and `category` as a `distinct` value on count)
- `GET/POST /api/v1/orgs/{org_id}/setting/{app_name}/link_accounts` (VMware): added optional `cloud_name` (Workspace ONE UEM datacenter: `na`, `emea`, `apac`, `uat`; when omitted each datacenter is tried in turn) to the `account_vmware_config` request schema; `400` `Invalid cloud_name` documented; `cloud_name` in the linked accounts response now also returned for VMware (`account_oauth_info_account.cloud_name` description clarified)
- `GET/POST /api/v1/orgs/{org_id}/setting/{app_name}/link_accounts`, `PUT/DELETE /api/v1/orgs/{org_id}/setting/{app_name}/link_accounts/{account_id}`: added the `infoblox` application (Infoblox CSP): `oauth_app_name` now includes `infoblox`; added `account_infoblox_config` (`api_key`, optional `cloud_name` `us`/`eu`) to the `account_oauth_add` request; added `account_oauth_update` (`account_oauth_config` or `account_infoblox_update`) as the `PUT` request, with the `OauthAppLinkUpdated` response (`account_infoblox_update_response`, only the updated account); `account_oauth_info_account`: added `csp_id`, `expires_at` and `infoblox_account_id`; Infoblox `400` errors documented
- `GET/POST /api/v1/orgs/{org_id}/setting/{app_name}/link_accounts` (CrowdStrike): `region` (CrowdStrike cloud region, e.g. `us-1`, `eu-1`) is now also returned for CrowdStrike accounts (`account_oauth_info_account.region` description clarified; previously Prisma only)
- `POST /api/v1/orgs/{org_id}/networktemplates`, `GET/PUT /api/v1/orgs/{org_id}/networktemplates/{networktemplate_id}` and `GET/PUT /api/v1/sites/{site_id}/setting` (`switch_matching_rule` schema): added AOS-CX only `aoscx_internal_vlan_range` (`N-M` VLAN IDs reserved for routed-only ports/L3 LAGs)
- `POST /api/v1/orgs/{org_id}/sitetemplates`, `GET/PUT /api/v1/orgs/{org_id}/sitetemplates/{sitetemplate_id}` (`site_template` schema): added `rftemplate_id`, `aptemplate_id`, `secpolicy_id`, `alarmtemplate_id`, `networktemplate_id`, `gatewaytemplate_id`, `routertemplate_id` (backfilled to sites that have not set them) and `sitegroup_ids` (added to the membership of sites using the template)
- Added `GET/POST /api/v1/orgs/{org_id}/zonepolicies` and `GET/PUT/DELETE /api/v1/orgs/{org_id}/zonepolicies/{zonepolicy_id}` (Org-level zone policies allowing or denying traffic from `from_zones` to `to_zones` for `tenants` and `services`, `action` defaults to `allow`); added `zonepolicy` and `zonepolicies` schemas, `ZonePolicy` and `ZonePoliciesArray` responses, `zonepolicy_id` path parameter, and the `Orgs Zone Policies` tag
- `POST /api/v1/orgs/{org_id}/gatewaytemplates`, `GET/PUT /api/v1/orgs/{org_id}/gatewaytemplates/{gatewaytemplate_id}` (`gateway_template` schema): added SRX-only `enable_zone_based_policies` (generate the security policy from zone policies instead of `service_policies`) and `snmp_config` (reuses the `snmp_config` schema)
- `gateway_mnha_config` schema (gateway templates and `device_gateway`): added `icl` (`back_to_back`, `encrypted`) and `redundancy_groups` (override-only SRG settings: `primary_node`, `probe_host`); added `gateway_mnha_config_icl`, `gateway_mnha_config_redundancy_group` and `gateway_mnha_config_redundancy_groups` schemas
- `gateway_matching_rule` schema (gateway templates and gateway device profiles): added `match_node` (`node0`/`node1`, per-node MNHA rules) and `ip_configs`
- `gateway_port_config` schema: added `ha_link` port `usage`; `gateway_port_config_ip_config`: added `mnha_vip`
- `GET /api/v1/orgs/{org_id}/stats/assets/search`: added `altbeacon_uuid`, `altbeacon_major`, `altbeacon_minor` and `by` query parameters
- `GET /api/v1/orgs/{org_id}/stats/assets/count` (`org_asset_count_distinct` schema): `distinct` now also accepts `altbeacon_major`, `altbeacon_minor`, `altbeacon_uuid`, `by`, `device_name`, `eddystone_uid_instance`, `eddystone_uid_namespace`, `eddystone_url` and `name`; default is `site_id`
- `GET/POST /api/v1/orgs/{org_id}/pskportals`, `GET/PUT /api/v1/orgs/{org_id}/pskportals/{pskportal_id}` (`psk_portal` schema): added optional `vlan_name` (`vlan_id` takes precedence when both are set)
- `GET /api/v1/orgs/{org_id}/devices/last_config/search`: added `cert_expiry` (all device types) and device-type specific filters, AP: `ssids`, `ssids_6`, `ssids_5`, `ssids_24`, `channel_5`, `channel_6`, `channel_24`, `radio_macs`, `secpolicy_violated`, `wlan_ids`, `errors`, `uses_mxtunnel`; switch: `evpntopo_id`, `evpntopo_role`, `evpntopo_type`, `evpntopo_as`, `networks`, `vrfs`; gateway: `services`, `networks`, `lan_networks`, `servicepolicies`, `securityzones`, `zones`, `zonepolicies`, `idpprofiles`
- `GET /api/v1/const/alarm_defs` (`const_alarm_definition` schema): added `default_enabled` (whether the alarm type is enabled by default)
- `GET /api/v1/orgs/{org_id}/stats/mxedges`, `GET /api/v1/orgs/{org_id}/stats/mxedges/{mxedge_id}`, `GET /api/v1/sites/{site_id}/stats/mxedges`, `GET /api/v1/sites/{site_id}/stats/mxedges/{mxedge_id}` (`stats_mxedge_oob_ip_stat` schema, `oob_ip_stat`): added `ifname`, `mac`, `speed`, `full_duplex`, `mtu`, `tx_bytes`, `tx_pkts`, `tx_errors`, `tx_dropped`, `rx_bytes`, `rx_pkts`, `rx_errors`, `rx_dropped`, `rx_multicast` and `lldp_nd` (new `stats_mxedge_oob_ip_stat_lldp_nd` schema); fixed the IPv6 assignment mode property name `type8` → `type6`
- `GET /api/v1/orgs/{org_id}/stats/mxedges`, `GET /api/v1/orgs/{org_id}/stats/mxedges/{mxedge_id}`, `GET /api/v1/sites/{site_id}/stats/mxedges`, `GET /api/v1/sites/{site_id}/stats/mxedges/{mxedge_id}` (`stats_mxedge` schema): added `tunterm_mac` (MAC of the tunterm datapath's host-side bridge, `kni0` virtual interface)
- Added `GET /api/v1/orgs/{org_id}/stats/vtep_peers/search` and `GET /api/v1/orgs/{org_id}/stats/vtep_peers/count` (VTEP peer stats: local `ip`, `peer_ip`, `peer_mac`, packet and byte counters); added `vtep_peer_stats_search_result`, `vtep_peer_stats_search_results`, `vtep_peer_stats_search_results_items` and `vtep_peer_stats_count_distinct` schemas, the `VtepPeersStatsSearch` response, and the `Orgs Stats - VTEP Peers` tag
- `GET /api/v1/orgs/{org_id}/stats/ospf_peers/count`: added `state` filter
- `POST /api/v1/orgs/{org_id}/devices/upgrade` (`upgrade_org_devices` schema): `device_type` now also accepts `router` (Junos MX devices); added `upgrade_org_devices_device_type` schema
- `GET /api/v1/orgs/{org_id}/nac_clients/events/search`: added `nas_ip6` filter (IPv6 address of the NAS device)
- `GET /api/v1/orgs/{org_id}/nac_clients/search`: added `nas_ip6` filter (IPv6 address of the NAS device)
- `GET /api/v1/sites/{site_id}/nac_clients/events/search` and `GET /api/v1/sites/{site_id}/nac_clients/search`: added `nas_ip6` filter (IPv6 address of the NAS device)
- `GET /api/v1/orgs/{org_id}/setting/mist_scep/client_certs` (`issued_client_certificates_results` schema): added `start`, `end` and `total`; `limit` maximum documented as 1000 (default 100)
- `GET /api/v1/orgs/{org_id}/setting/mist_scep/events/search`: documented the meaning of the `type` values (`failure`, `success`)
- `GET/POST /api/v1/sites/{site_id}/wlans`, `GET/PUT /api/v1/sites/{site_id}/wlans/{wlan_id}` and the org WLAN endpoints (`wlan` schema): added `enable_mlo` (Multi-Link Operation) and `timezone_ie` (Time Zone information element); `wlan_auth` schema: added `disable_gtk_rekey` (only honored on AP firmware < 0.15)
- `POST /api/v1/sites/{site_id}/maps/{map_id}/wayfinding/import` (`wayfinding_import_json` schema): added MazeMap (`vendor_name`==`maze_map`) import with `url`, `config` or `campus_id` (one is required), `view_access_token`, `building_id` and `floor_id`; added `map_maze_map` and `map_maze_map_vendor_name` schemas
- `GET/POST /api/v1/orgs/{org_id}/assetfilters`, `GET/PUT /api/v1/orgs/{org_id}/assetfilters/{assetfilter_id}`, `GET/POST /api/v1/sites/{site_id}/assetfilters`, `GET/PUT /api/v1/sites/{site_id}/assetfilters/{assetfilter_id}` (`asset_filter` schema): added `altbeacon_uuid` and `altbeacon_major` filter properties
- Asset stats endpoints (`GET /api/v1/orgs/{org_id}/stats/assets`, `GET /api/v1/orgs/{org_id}/stats/assets/search`, `GET /api/v1/sites/{site_id}/stats/assets`, `GET /api/v1/sites/{site_id}/stats/assets/search`, `GET /api/v1/sites/{site_id}/stats/assets/{asset_id}`; `stats_asset` schema): added `altbeacon_uuid`, `altbeacon_major` and `altbeacon_minor`
- `GET /api/v1/sites/{site_id}/stats/maps/{map_id}/discovered_assets`: added optional `duration` query parameter (time duration TTL filter in seconds, 60-86400, default 60); the response also returns `altbeacon_uuid`, `altbeacon_major` and `altbeacon_minor` (`stats_asset` schema)
- `GET /api/v1/sites/{site_id}/stats/assets/search`: added `altbeacon_uuid`, `altbeacon_major` and `altbeacon_minor` query parameters
- `GET /api/v1/sites/{site_id}/stats/assets/count` (`site_assets_count_distinct` schema): `distinct` now also accepts `altbeacon_major`, `altbeacon_minor`, `altbeacon_uuid` and `site_id`; default changed from `map_id` to `site_id`
- `PUT /api/v1/sites/{site_id}/devices/{device_id}` (`device_ap` schema): added `vostio` (Vostio/ASSA ABLOY ZigBee networks keyed by netId: `name`, `broker_endpoint`, `port`, `client_cert`, write-only `client_key`; new `ap_vostio`, `ap_vostio_network` and `ap_vostio_networks` schemas, device level only, not available on AP device profiles); `ap_zigbee` (`zigbee_config`, also used by AP device profiles): added `type` (`visionline`/`vostio`), `vostio_network_id`, `power_mode` (`default`/`custom`) and `power`; `ap_aeroscout` (`aeroscout`, also used by AP device profiles): added `locate_ble`; `locked` description corrected
- AP radio `antenna_mode` (device, device profile and RF template bands): `1x4` is now accepted (`ap_radio_antenna_mode` and `radio_band_antenna_mode` schemas)
- AP device config (`ap_esl_config`, `ap_usb`): `vusion` added to the ESL and USB integration `type` enums (`ap_esl_type`, `ap_usb_type`) and to the `vlan_id` note; `channel` documented as 0-10; `ap_aeroscout.locate_ble` description now notes only company-id 935 manufacturer data is forwarded
- `PUT /api/v1/sites/{site_id}/devices/{device_id}` (`device_switch` schema): added AOS-CX only `aoscx_internal_vlan_range`; `oob_ip_config` (`switch_oob_ip_config`, also used by switch device profiles): added `node1` (new `switch_oob_ip_config_node1` schema) and clarified `use_mgmt_vrf` (ignored on AOS-CX) and `use_mgmt_vrf_for_host_out`; `radius_config` (`switch_radius_config`): added `no_resolve_radius_hostname`
- Switch `extra_routes` (`extra_route` schema; device, device profile, network template and site setting): added `tag` (AOS-CX `1-4294967295`); `metric` and `preference` maximum raised from 2147483647 to 4294967295
- Switch routing policies (`sw_routing_policy_term_matching` schema): added `tag` list of route tags to match (AOS-CX, `1-4294967295`)
- Added `GET /api/v1/sites/{site_id}/devices/{device_id}/derived` (fully-merged, read-only intent configuration of an AP, switch or gateway, resolved across the configuration inheritance hierarchy; secrets masked with `********`); added the `response_device_derived_config` schema and the `DeviceDerivedConfig` response
- `PUT /api/v1/sites/{site_id}/devices/{device_id}` (`device_switch` schema): `vrf_config` now has `vrfs` (per-device, per-VRF `loopback_ip`; non-EVPN, in EVPN these are auto-assigned via `evpn_auto_loopback_subnet`); the switch device uses the new `switch_vrf_config` schema (with `switch_vrf_config_vrfs` and `switch_vrf_config_vrf`), other objects keep `vrf_config`
- Added `POST /api/v1/sites/{site_id}/devices/{device_id}/add_gbp_tag` and `POST /api/v1/sites/{site_id}/devices/{device_id}/remove_gbp_tag` (incrementally add or remove GBP tags for wired-client MACs on a switch; request is a `{mac: gbp_tag}` map, `1`-`65535`, at most 8000 MACs, all-or-nothing; `400` lists every invalid entry); added `utils_add_gbp_tag`, `utils_remove_gbp_tag` and `response_device_gbp_tag_invalid` schemas and the `DeviceGbpTagInvalid` response
- `GET /api/v1/sites/{site_id}/devices/versions`: `type` now also accepts `router` (Junos firmware for MX routers only, no AOS-CX; new `device_versions_type` schema); added `family` query parameter (e.g. `aoscx`, `junos`); `model` also applies to router devices
- `GET /api/v1/const/device_models` (`const_device_switch` schema): added `skus`, `aoscx_device`, `cx_l2_only` (AOS-CX L2 plus static routes/SVIs only, defaults to `false`), `has_qos_dwrr` (AOS-CX DWRR QoS support), `has_oob` (dedicated OOB management port; also on `const_device_gateway`) and `max_slots`; AOS-CX examples added; DFS descriptions of `fcc_dfs_ok`, `ce_dfs_ok` and `other_dfs_ok` clarified (US, EU, JP + other); fixed the `const_device_model` discriminator mapping (`gateway` and `switch` were swapped)
- `GET/POST /api/v1/orgs/{org_id}/wxtags`, `GET/PUT /api/v1/orgs/{org_id}/wxtags/{wxtag_id}`, `GET/POST /api/v1/sites/{site_id}/wxtags`, `GET/PUT /api/v1/sites/{site_id}/wxtags/{wxtag_id}` (`wxlan_tag` schema): added the `gbp_resource` tag `type` (GBP-tagged local wireless peer, `dst_allow_wxtags` / `dst_deny_wxtags` only) with `gbp_tags` (1-65535, empty matches any local peer) and optional `specs`; added the `gbp_tag` `match` (client's own GBP tag from RADIUS, `src_wxtags`)
- Added `GET /api/v1/sites/{site_id}/zonepolicies/derived` and `GET /api/v1/sites/{site_id}/securityzones/derived` (derived Zone Policies and Security Zones for a site, optional `resolve` to resolve the site variables); added the `Sites Zone Policies` and `Sites Security Zones` tags
- Switch settings (site setting, network template, device profile and switch device; `switch_mgmt`, `switch_network_multicast`, `switch_port_usage` schemas): added `switch_mgmt.enable_hw_resource_monitor` (alarm before a forwarding table fills up), `networks.<name>.multicast.disable_pim` (non-EVPN only; boolean or variable), and port usage `mcast_router_link` and `keep_session_for_idle_client`
- `GET/PUT /api/v1/sites/{site_id}/setting` (`site_setting` schema): added `mnha_config` (reuses `gateway_mnha_config`, inherited by both MNHA node devices); `gateway_mnha_config`: added `node_macs` (cluster membership, positional: index 0 is `node0`, index 1 is `node1`)
- `GET /api/v1/sites/{site_id}/setting/derived`: added `device_type` query parameter; for `router` the router also inherits the Network (switch) template (`switch_mgmt` / `switch_matching`) and uses the `switch` sub-node in the site settings as a base, with its own `router` sub-node overriding conflicting keys
- Org and site webhooks (`webhook` schema): `rules` is now a per-topic map `{topic: [rule]}` (was a flat list of rules with `topic`), rule `action` is `accept` / `drop` (was `permit` / `block`; new `webhook_rule_action` and `webhook_rule_list` schemas), `matching` is optional and the `topic` property is removed from `webhook_rule`; the first matching rule is applied and messages matching no rule are accepted; `default_action` deprecated
- Wireless client stats (`GET /api/v1/sites/{site_id}/stats/clients`, `GET /api/v1/sites/{site_id}/stats/maps/{map_id}/clients`, `GET /api/v1/sites/{site_id}/stats/devices/{device_id}/clients`; `stats_wireless_client` schema): added `os_type`, `os_version`, `hardware` and `firmware` (through fingerprinting)
- Added `GET /api/v1/sites/{site_id}/flows/search` (search network flows across all switch devices of a site, with `device_mac` filter); **breaking:** `GET /api/v1/sites/{site_id}/devices/{device_id}/flow_records/search` moved to `GET /api/v1/sites/{site_id}/devices/{device_id}/flows/search` (operation `searchSiteDeviceFlowRecords` renamed `searchSiteDeviceFlows`)
- `GET /api/v1/sites/{site_id}/stats/discovered_switches/search` and `GET /api/v1/sites/{site_id}/stats/discovered_switches/count`: added `device_type` filter (`ap`, `camera`, `digital_signage`, `endpoint`, `gateway`, `switch`, `unknown`, `voip`; new `discovered_device_type` schema); `count` `distinct` also accepts `device_type`, `hostname` and `vendor`, and its default changed from `system_name` to `hostname`; `discovered_switch` schema: added `hostname` and `device_type`
- `GET /api/v1/sites/{site_id}/stats/ports/search`: added `port_ips` filter; switch and gateway port stats (`stats_switch_port` and `stats_gateway_port` schemas): added `port_ips` (IP addresses on the interface)
- `POST /api/v1/sites/{site_id}/analyze_spectrum`: the websocket stream example output now includes `device_id` and `sweep`
- `GET /api/v1/sites/{site_id}/rrm/events` (`rrm_event` schema): added `audit_id` (audit log ID of a user-triggered RRM optimization)
- `GET /api/v1/const/applications`: added optional `device_type` query parameter (`ap`, `gateway`; new `const_applications_device_type` schema) to filter to applications identifiable by a device family; `app_probe` and `app_id` descriptions clarified
- Added `GET /api/v1/sites/{site_id}/stats/vtep_peers/search` and `GET /api/v1/sites/{site_id}/stats/vtep_peers/count` (site-level VTEP peer stats, same schemas as the org-level endpoints); added the `Sites Stats - VTEP Peers` tag
- `GET /api/v1/sites/{site_id}/stats/ospf_peers/count`: added `state` filter
- `GET /api/v1/sites/{site_id}/stats/calls/troubleshoot` (`call_troubleshoot_summary` schema): added `radio_noise_floor`, `client_rx_exhausted`, `switch_if_flap` and `switch_if_rx_errors_per_gb` contributor metrics
- Added the `oauth2` security scheme (OAuth2 authorization code flow with PKCE and rotating refresh tokens, `authorizationUrl` `/api/v1/orgs/oauth/authorize`, `tokenUrl` and `refreshUrl` `/api/v1/orgs/oauth/token`, no fixed scopes) and added it to the global `security` (`Authorization: Bearer <access_token>`); `GET/POST /api/v1/orgs/oauth/authorize` explicitly use the login session (`csrfToken`)
- Merged PR #77: 22 public `/api/v1/const/` endpoints (`alarm_defs`, `ap_led_status`, `app_categories`, `app_subcategories`, `applications`, `client_events`, `countries`, `device_events`, `fingerprint_types`, `gateway_applications`, `languages`, `license_types`, `marvisclient_events`, `marvisclient_versions`, `mxedge_events`, `mxedge_models`, `nac_events`, `otherdevice_events`, `otherdevice_models`, `system_events`, `traffic_types`, `webhook_topics`) now document that authentication is optional (`security` is anonymous, `apiToken`, `csrfToken` or `oauth2`)
- Merged PR #76: updated the `info.description` links (removed the API Sandbox and Exercises and Juniper Blog links, added the HPE Community link and the Safari App Store link for the Mist Web Browser Extension)
- `GET /api/v1/orgs/{org_id}/inventory`: the `model` query parameter accepts the special value `mutable` to list devices whose model can be changed with `update_model`
- `switch_port_usage_reauth_interval` schema (`reauth_interval` of switch `port_usages`: network template, site setting and switch device): added an integer alternative restricted to `0` (disable reauthentication) next to the existing 10-65535 range, so `1`-`9` stay invalid; description clarified (MIST-239706)

## [2610.1.0] - 2026-10-01

- `switch_mgmt` (switch, network/switch templates, and device profile schemas) `radius` setting: replaced the nested `radius_config` object with top-level `auth_servers`, `auth_servers_retries`, `auth_servers_timeout`, and `network` fields; `use_different_radius` changed from string to boolean; added `switch_mgmt_radius_auth_server`/`switch_mgmt_radius_auth_servers` schemas (`auth_servers` items include a read-only `id`); `auth_servers`, `auth_servers_retries`, and `auth_servers_timeout` are required when `enabled`==`true` and `use_different_radius`==`true`
- `ap_radio_band24`/`ap_radio_band5`/`ap_radio_band6` and `rftemplate_radio_band24`/`rftemplate_radio_band5`/`rftemplate_radio_band6` schemas: `power_min` minimum lowered to `0` (previously `3` for 2.4 GHz, `5` for 5/6 GHz) to allow a minimum transmit power of 0 dBm

## [2609.1.0] - 2026-09-07

- Fixed `GET /api/v1/sites/{site_id}/insights/fingerprints/count` and `GET /api/v1/sites/{site_id}/insights/fingerprints/search`: moved to `GET /api/v1/orgs/{org_id}/insights/fingerprints/count` and `GET /api/v1/orgs/{org_id}/insights/fingerprints/search` (these endpoints only ever worked at the org level; incorrectly documented under sites)
- Added `GET /api/v1/orgs/{org_id}/vars/count` (distinct count of organization vars, grouped by `site_id`, `src`, or `var`)
- Added `GET/PUT/DELETE /api/v1/sites/{site_id}/mapstacks/{mapstack_id}`; replaced `map.group_name`/`map.group_idx` with `mapstack_id`/`mapstack_floor`
- `POST /api/v1/register` (`admin_invite` schema): added optional `no_tracking` privacy-consent setting with GDPR-dependent default behavior
- `GET /api/v1/sites/{site_id}/stats/calls/count`: added `mac` and `ap_mac` filters; `rating` now accepts comma-separated values
- `GET /api/v1/sites/{site_id}/rrm/channel_scores/band/{band}`: added optional `ap` query parameter to return per-AP channel scores
- `GET /api/v1/orgs/{org_id}/inventory/search`: added `vc_mac`, `master_mac`, `modified_after`, `disconnected_before` query parameters
- `GET /api/v1/orgs/{org_id}/inventory/search` (`inventory_search_result` schema): added `timestamp`, `last_name_change`, `last_disconnected`
- `GET /api/v1/orgs/{org_id}/inventory/search` (`inventory_search` schema): `start` and `end` changed from integer to number (epoch seconds with fractional part)
- `POST /api/v1/orgs/{org_id}/networks`, `GET/PUT /api/v1/orgs/{org_id}/networks/{network_id}` (`network` schema): added optional `zone_id` (SecurityZone UUID; when omitted the network `name` is used as the security zone name)
- Added `GET/POST /api/v1/orgs/{org_id}/securityzones` and `GET/PUT/DELETE /api/v1/orgs/{org_id}/securityzones/{securityzone_id}` (Org-level SRX security zones); added `securityzone` and `securityzones` schemas, `SecurityZone` and `SecurityZonesArray` responses, and the `Orgs Security Zones` tag
- `POST /api/v1/orgs/{org_id}/gatewaytemplates`, `GET/PUT /api/v1/orgs/{org_id}/gatewaytemplates/{gatewaytemplate_id}` (`gateway_template` schema) and `PUT /api/v1/sites/{site_id}/devices/{device_id}` (`device_gateway` schema): added `mnha_config`; added `gateway_mnha_config` schema (SRX Multi-Node HA, replaces chassis-cluster mode when enabled)
- `POST /api/v1/orgs/{org_id}/pcaps/capture` (`capture_mxedge` schema): `max_pkt_len` maximum lowered from 2048 to 1536
- `GET /api/v1/orgs/{org_id}/stats/mxedges`, `GET /api/v1/orgs/{org_id}/stats/mxedges/{mxedge_id}`, `GET /api/v1/sites/{site_id}/stats/mxedges`, `GET /api/v1/sites/{site_id}/stats/mxedges/{mxedge_id}` (`stats_mxedge` schema): added `drop_stat`; added `stats_mxedge_drop_stat` schema
- `GET /api/v1/orgs/{org_id}/stats/bgp_peers/search` and `GET /api/v1/sites/{site_id}/stats/bgp_peers/search` (`bgp_stats` schema): added `flap_count` and `router_id`
- `GET /api/v1/orgs/{org_id}/stats/ospf_peers/search` and `GET /api/v1/sites/{site_id}/stats/ospf_peers/search` (`ospf_peer_stats_search_results_items` schema): renamed `peer_ip` → `neighbor` (`peer_ip` kept and marked deprecated); added `neighbor_id`
- Added `GET /api/v1/orgs/{org_id}/setting/mist_scep/events/search` (Mist SCEP PKI operation events); added `scep_event`, `scep_events`, `scep_event_type`, `org_scep_events_search_type` and `response_scep_events_search` schemas, and the `ScepEventsSearch` response
- `POST /api/v1/sites/{site_id}/pcaps/capture` (`capture_max_pkt_length` schema): maximum `max_pkt_len` lowered from 2048 to 1536
- `GET/POST /api/v1/orgs/{org_id}/assetfilters`, `GET/PUT /api/v1/orgs/{org_id}/assetfilters/{assetfilter_id}`, `GET/POST /api/v1/sites/{site_id}/assetfilters`, `GET/PUT /api/v1/sites/{site_id}/assetfilters/{assetfilter_id}` (`asset_filter` schema): added `aeroscout_forwarding`
- `switch_multicast_config` (network templates, device profiles, site settings, and device configuration): added `rp_mac`, `peg_enabled`, and `sbd_wan_rpf`; clarified `anycast_rp` / `rp_ip` precedence and EVPN RP behavior
- `switch_port_usage` (site settings and other shared switch port-usage configurations): added optional `no_local_port_config` (boolean, default `false`) to control whether the usage can be overridden in local port configuration
- `GET/PUT /api/v1/sites/{site_id}/setting` and `GET /api/v1/sites/{site_id}/setting/derived` (`site_setting_paloalto_networks`, `site_setting_juniper_srx` schemas): added optional `mist_nac_user_role_source` enum (`idp_role`, `radius_group`, `none`), defaulting to `idp_role`
- `synthetictest_config_wan_speedtest` (`GET/PUT /api/v1/orgs/{org_id}/setting`, `GET/PUT /api/v1/sites/{site_id}/setting`, and `GET /api/v1/sites/{site_id}/setting/derived`): renamed `enabled` to `disabled` and set the default to `false`
- `switch_port_usage` (`mac_auth_protocol`): clarified Mist NAC behavior; the protocol is forced to `pap` unless `mist_nac.enable_eap_md5_for_mab` preserves `eap-md5` for EAP-MD5 over MAB
- Added `GET/POST/DELETE /api/v1/sites/{site_id}/flow_capture` with Flow Capture session, request, normalized stream message, and status response schemas; request validation requires `switches` plus at least one flow filter
- `POST /api/v1/sites/{site_id}/analyze_spectrum` (`spectrum_analysis` schema): added multi-AP `device_ids` (maximum 5, takes precedence over `device_id`); extended duration maximum from 600 to 3600 seconds; added `SpectrumAnalysisSession` response with `session_id` and optional `invalid_device_ids`
- `POST /api/v1/sites/{site_id}/analyze_spectrum` (`spectrum_analysis_response` schema): added `started_time`, `device_id`/`device_ids`, `duration`, `band`, `format`, `width`, and `channels`; added multi-AP `invalid_device_ids`
- `GET /api/v1/sites/{site_id}/stats/analyze_spectrum` (`response_past_spectrum_analysis_result` schema): added optional `device_id`/`device_ids` identifiers, with a maximum of 5 devices (both remain optional; legacy records identified only by `mac` are still valid)

## [2607.1.1] - 2026-08-17

- `GET /api/v1/orgs/{org_id}/jsi/inventory/search` (`warranty_type` query parameter and `js_inventory_item.warranty_type`): changed from a fixed enum to a string to support all warranty values returned by Juniper Support Insight.
- `GET /api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metric/{metric}/impacted-applications`, `GET /api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metric/{metric}/impacted-aps`, and `GET /api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metric/{metric}/impacted-users`: response `limit` fields are now integers.

## [2607.1.0] - 2026-07-21

- `GET/PUT /api/v1/orgs/{org_id}/setting` (`org_setting_api_policy` schema): added `enforce_src_ips_for_tokens`
- `GET/PUT /api/v1/orgs/{org_id}/setting` (`org_setting` schema): added `cacerts_configs`; removed `cradlepoint`; removed `org_setting_cradlepoint` schema
- Added `org_setting_cacerts_config` and `org_setting_cacerts_configs` schemas
- `GET/PUT /api/v1/orgs/{org_id}/setting` (`org_setting_mist_nac` schema): added `enable_eap_md5_for_mab`
- `GET /api/v1/orgs/{org_id}/setting/cradlepoint/setup` (`test_cradlepoint` schema): added `alert_config_id`, `cp_api_id`, `cp_api_key`, `destination_config_id`, `ecm_api_id`, `ecm_api_key`, `enable_lldp`, `shared_secret`
- `GET/PUT/DELETE /api/v1/orgs/{org_id}/rftemplates/{rftemplate_id}` (`rf_template` schema): added `enable_unii_4`
- `POST /api/v1/orgs/{org_id}/networktemplates`, `GET/PUT/DELETE /api/v1/orgs/{org_id}/networktemplates/{networktemplate_id}` (`snmpv3_config_notify_filter_item` schema): added `categories`; added `snmpv3_config_notify_filter_item_categories` schema
- `POST /api/v1/orgs/{org_id}/gatewaytemplates`, `GET/PUT/DELETE /api/v1/orgs/{org_id}/gatewaytemplates/{gatewaytemplate_id}` (`gateway_wan_probe_override` schema): added `hostnames`, `http`; added `gateway_wan_probe_override_http` schema
- `POST /api/v1/orgs/{org_id}/gatewaytemplates`, `GET/PUT/DELETE /api/v1/orgs/{org_id}/gatewaytemplates/{gatewaytemplate_id}` (`tunnel_config_node` schema): added `internal_ip6s`, `probe_hostnames`, `probe_http`, `probe_ip6s`; added `tunnel_config_node_probe_http` schema
- `POST /api/v1/orgs/{org_id}/gatewaytemplates`, `GET/PUT/DELETE /api/v1/orgs/{org_id}/gatewaytemplates/{gatewaytemplate_id}` (`gw_routing_policy_term_action` schema): added `next_policy`, `next_term`
- `PUT /api/v1/orgs/{org_id}/psks` and `POST /api/v1/orgs/{org_id}/psks` (`psk` schema): added `usermac_labels` field and `usermac_labels` value to `psk_usage` enum; added `psk_usermac_labels` schema
- `GET /api/v1/orgs/{org_id}/devices/events/search` and `GET /api/v1/sites/{site_id}/devices/events/search`: added `job_id`, `status`, `template_id`, `tunnel_name` fields to `device_event` schema
- `GET /api/v1/sites/{site_id}/iotendpoints/count`: added `ap_mac`, `mac`, `type` values to `distinct` query parameter enum (`site_iotendpoints_count_distinct` schema)
- `GET /api/v1/orgs/{org_id}/devices/events/count`: added `includes` query parameter
- `GET /api/v1/orgs/{org_id}/mxedges/{mxedge_id}/stats`, `GET /api/v1/sites/{site_id}/mxedges/{mxedge_id}/stats` (`stats_mxedge` schema): added `kernel_abi`, `kernel_version`
- `GET /api/v1/orgs/{org_id}/stats/tunnels/search` (`stats_mxtunnel` schema): added `start_time`; removed `uptime`, `rx_control_pkts`, `tx_control_pkts`
- Added `GET /api/v1/orgs/{org_id}/aoscx/register_cmd` (replaces `aos/register_cmd`); added `aoscx_register_cmd` schema
- Removed `GET /api/v1/orgs/{org_id}/aos/register_cmd`
- `POST /api/v1/orgs/{org_id}/ssr/upgrade` and `POST /api/v1/sites/{site_id}/devices/{device_id}/upgrade` (`ssr_upgrade`, `ssr_upgrade_multi` schemas): added `force`
- `GET /api/v1/orgs/{org_id}/ssr/upgrade` and `GET /api/v1/orgs/{org_id}/ssr/upgrade/{upgrade_id}` (`response_ssr_upgrade`, `response_ssr_upgrade_status` schemas): added `force`; added `strategy` to `response_ssr_upgrade_status`
- `GET /api/v1/orgs/{org_id}/nac_clients/search`: renamed `edr_provider` → `edr_providers` query parameter
- `GET /api/v1/orgs/{org_id}/nac_clients/count`: renamed `distinct` enum value `edr_provider` → `edr_providers`
- `client_nac` schema: renamed `edr_provider` → `edr_providers` (array); `edr_status` now array
- `org_nac_clients_count_distinct` schema: renamed enum value `edr_provider` → `edr_providers`
- `user_mac` schema: added `site_ids`
- `GET /api/v1/const/marvisclient_events`: added new endpoint; added `const_marvisclient_event`, `const_marvisclient_events` schemas, `ConstMarvisClientEvents` response
- `nac_portal` schema: added `enable_location`
- `wlan_dynamic_psk` schema: added `local_vlan_ids`
- `PUT /api/v1/sites/{site_id}/devices/{device_id}` (`device_ap` schema): added `enable_unii_4`, `uwb_config`; added `ap_uwb_config` schema
- `deviceprofile_ap` schema: added `uwb_config`
- `ap_mqtt` schema: added `default_topic`
- `acl_policy` schema: added `disabled`
- `acl_tag_type` schema: added `aruba_user_role` enum value
- `network_template` schema: added `multicast_config`; added `switch_multicast_config` schema (`anycast_rp`, `rp_ip`, `sbd_vlan_id`, `sbd_subnet`)
- Added `DELETE /api/v1/sites/{site_id}/devices/{device_id}/zigbee_join`
- Added `POST /api/v1/sites/{site_id}/devices/{device_id}/zigbee_kick`; added `utils_zigbee_kick` schema
- Added `POST /api/v1/sites/{site_id}/devices/{device_id}/zigbee_event_trail`
- Added `POST /api/v1/sites/{site_id}/devices/{device_id}/zigbee_packet_trail`
- Added `zigbee_trail_response` schema and `ZigbeeTrail` response
- `GET /api/v1/orgs/{org_id}/jsi/pbn/search`: added `text`, `sort` query parameters; added enum values to `customer_risk`, `bug_type`; changed `jsi_pbn_item.product_family` to array; added `JsiPbnSearchExample`
- `GET /api/v1/orgs/{org_id}/jsi/sirt/search`: added enum values to `severity`; added `JsiSirtSearchExample`
- `POST /api/v1/orgs/{org_id}/devices/upgrade` (`upgrade_org_devices` schema): added `enable_p2p`, `version` (deprecated); added `ssr` to `upgrade_org_devices_version_firmware_type` enum
- `GET /api/v1/orgs/{org_id}/jsi/inventory/search`: added `contract_end_before`, `contract_end_after`, `contract_type`, `contract_sku`, `end_of_service_time`, `support_contract_status` query parameters; added `contract_id`, `contract_sku`, `end_of_service_time`, `support_contract_status` fields to `js_inventory_item` schema
- Site Setting networks (`switch_network` schema): added `multicast`; added `switch_network_multicast` schema
- Site Setting vrf_instances (`switch_vrf_instance` schema): added `multicast_config`
- Site Setting gateway_mgmt (`gateway_mgmt` schema): added `disable_idp_pcap`
- Site Setting (`site_setting` schema): added `uwb_config`
- Webhooks (`webhook` schema, Org and Site): added `rules`, `default_action`; added `webhook_rules`, `webhook_rule`, `webhook_rule_matching`, `webhook_action` schemas
- `GET /api/v1/sites/{site_id}/stats/devices` (`stats_ap` schema): added `zigbee_stat`; added `stats_ap_zigbee_stat` schema
- `GET /api/v1/sites/{site_id}/stats/clients`, `GET /api/v1/sites/{site_id}/stats/maps/{map_id}/clients`, `GET /api/v1/sites/{site_id}/stats/devices/{device_id}/clients` (`stats_wireless_client` schema): added `mxedge_id`
- Added `GET /api/v1/sites/{site_id}/iotendpoints/count`; added `site_iotendpoints_count_distinct` schema
- Added `POST /api/v1/sites/{site_id}/iotendpoints/{id}/zigbee_rejoin`
- Added `GET /api/v1/sites/{site_id}/devices/{device_id}/flow_records/search`; added `response_device_flow_records_search`, `flow_record` schemas, `DeviceFlowRecordsSearch` response, `DeviceFlowRecordsSearchExample`
- `GET /api/v1/sites/{site_id}/stats/analyze_spectrum` (`response_past_spectrum_analysis_result` schema): added `spectrogram_url`
- `GET /api/v1/const/license_types` (`const_license_type` schema): added `type`, `group`, `enforcement_level`, `entitled_licenses`
- `GET /api/v1/sites/{site_id}/stats/calls/troubleshoot`: added `wired` query parameter
- `GET /api/v1/sites/{site_id}/stats/calls/summary`: added `wired` query parameter

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
