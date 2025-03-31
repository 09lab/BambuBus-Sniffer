BBP_PKT_STX = 0x3D

BBP_PKT_IDX_FLAG = 1
BBP_LPKT_IDX_LENGTH = 4
BBP_LPKT_IDX_CRC8 = 6
BBP_LPKT_IDX_TGT_ADDR = 7
BBP_LPKT_IDX_SRC_ADDR = 9
BBP_LPKT_IDX_CONTENT = 11

BBP_SPKT_IDX_LENGTH = 2
BBP_SPKT_IDX_CRC8 = 3
BBP_SPKT_IDX_TYPE = 4
BBP_SPKT_IDX_CONTENT=5

BAMBU_FLAG_SET = {
    0: "RES",
    5: "REQ",
}

BAMBU_DEVICE_SET = {
    3: "MC",
    6: "AP",
    7: "AMS",
    8: "TH",
    9: "AP2",
    0xE: "AHB",
    0xF: "EXT",
    0x13: "CTC",
}

BAMBU_CMD_SET = {
    (1, 1): "ping",
    (1, 3): "get_version",
    (1, 4): "sync_timestamp",
    (1, 6): "mcu_upgrade",
    (1, 8): "mcu_hms",
    (1, 9): "factory_reset",
    (2, 4): "get ams serial",
    (2, 5): "gcode_execute_state",
    (2, 6): "gcode_request", # no official name for this
    (2, 9): "mcu_display_message",
    (2, 10): "vosync",
    (2, 11): "gcode_ctx",
    (2, 12): "mc_state",
    (2, 15): "link_ams_report",
    (2, 17): "ack_tray_info",
    (2, 22): "gcode_line_handle",
    (2, 23): "ams_mapping",
    (2, 24): "ams_tray_info_write_ack",
    (2, 25): "ams_user_settings",
    (2, 27): "hw_info_voltage",
    (2, 28): "link_ams_tray_consumption_ack",
    (2, 29): "pack_get_part_info_ack",
    (2, 34): "extrusion_result_update",
    (2, 36): "fila_ams_get",
    (2, 37): "mc_get_skipped_obj_list",
    (3, 1): "ams version and name",
    (3, 2): "M972 - check scanner clarity",
    (3, 5): "M963",
    (3, 7): "M969",
    (3, 6): "M965_b",
    (3, 9): "M967",
    (3, 11): "M973 - turn OFF scanner",
    (3, 14): "M965",
    (3, 49): "M976 - nozzle scan option",
    (3, 50): "M977 - scan_first_layer",
    (3, 51): "M978",
    (3, 52): "M981 - Spaghetti detector on/off",
    (3, 53): "M991 - notify layer change",
    (3, 81): "M987",
    (3, 82): "SENSORCHECK",
    (4, 1): "set_module_sn",
    (4, 2): "get_module_sn",
    (4, 3): "inject_module_key",
    (4, 4): "get_inject_status",
    (4, 5): "mcu_reboot",
    (4, 6): "send_to_amt_core",
    (4, 7): "set_module_lifecycle",
    (4, 8): "get_module_lifecycle",
    (4, 10): "inject_productcode",
    (4, 11): "get_productcode",
}
