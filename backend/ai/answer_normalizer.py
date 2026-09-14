def normalize_answer(step_id: str, user_message: str) -> str:
    """
    Converts natural-language user answers into
    the exact answer keys expected by the diagnostic engine.
    """

    message = user_message.lower().strip()

    # ==================================================
    # SAFETY QUESTION
    # ==================================================

    if step_id == "safety_check":

        # ----------------------------------------------
        # NOT SURE
        # ----------------------------------------------

        if any(
            phrase in message
            for phrase in [
                "not sure",
                "unsure",
                "i don't know",
                "i dont know",
                "im not sure",
                "i'm not sure",
                "i am not sure",
                "cannot tell",
                "can't tell",
            ]
        ):
            return "not sure"

        # ----------------------------------------------
        # DANGEROUS / YES
        # ----------------------------------------------

        if any(
            phrase in message
            for phrase in [
                "there are sparks",
                "there is a spark",
                "there is smoke",
                "there's smoke",
                "there is a burning smell",
                "there's a burning smell",
                "i smell burning",
                "i smell something burning",
                "it smells burnt",
                "it smells burned",
                "i got shocked",
                "i was shocked",
                "the device shocked me",
                "it shocked me",
                "there are exposed wires",
                "there is an exposed wire",
                "the wire is exposed",
                "the wires are exposed",
                "the cable is damaged",
                "the wire is damaged",
                "the plug is damaged",
                "the plug is burnt",
                "the plug is burned",
                "the socket is burnt",
                "the socket is burned",
                "there are burn marks",
                "it is melted",
                "it's melted",
                "it is overheating",
                "it's overheating",
            ]
        ):
            return "yes"

        # ----------------------------------------------
        # EXPLICIT YES
        # ----------------------------------------------

        if message in [
            "yes",
            "y",
            "yeah",
            "yep",
            "yes there is",
            "yes there are",
            "yes i do",
            "yes it does",
        ]:
            return "yes"

        # ----------------------------------------------
        # SAFE / NO
        # ----------------------------------------------

        if any(
            phrase in message
            for phrase in [
                "no sparks",
                "no spark",
                "no smoke",
                "no burning smell",
                "no burnt smell",
                "no burned smell",
                "no damage",
                "no visible damage",
                "no exposed wires",
                "no exposed wire",
                "no burn marks",
                "nothing looks damaged",
                "nothing appears damaged",
                "nothing is damaged",
                "everything looks fine",
                "everything seems fine",
                "everything is fine",
                "the cable is fine",
                "the plug is fine",
                "the wire is fine",
                "the wires are fine",
                "the socket is fine",
                "don't see any sparks",
                "dont see any sparks",
                "do not see any sparks",
                "don't see a spark",
                "dont see a spark",
                "do not see a spark",
                "don't see any smoke",
                "dont see any smoke",
                "do not see any smoke",
                "don't see any burning",
                "dont see any burning",
                "do not see any burning",
                "don't see any damage",
                "dont see any damage",
                "do not see any damage",
                "don't smell burning",
                "dont smell burning",
                "do not smell burning",
                "i don't smell burning",
                "i dont smell burning",
                "i do not smell burning",
                "nothing unusual",
                "nothing wrong with the cable",
                "nothing wrong with the plug",
            ]
        ):
            return "no"

        # ----------------------------------------------
        # EXACT NO
        # ----------------------------------------------

        if message in [
            "no",
            "n",
            "nope",
            "no there isn't",
            "no there is not",
            "no there are not",
            "no i don't",
            "no i do not",
            "no it doesn't",
            "no it does not",
        ]:
            return "no"

    # ==================================================
    # POWER SOURCE
    # ==================================================

    if step_id == "power_source":

        # NOT SURE
        if any(
            phrase in message
            for phrase in [
                "not sure",
                "unsure",
                "i don't know",
                "i dont know",
                "im not sure",
                "i'm not sure",
                "i am not sure",
                "cannot tell",
                "can't tell",
            ]
        ):
            return "not_sure"

        # NO POWER
        if any(
            phrase in message
            for phrase in [
                "no power",
                "there is no power",
                "there isn't any power",
                "there is not any power",
                "the socket is dead",
                "the socket doesn't work",
                "the socket does not work",
                "another appliance doesn't work",
                "another appliance does not work",
                "another device doesn't work",
                "another device does not work",
                "nothing works in the socket",
                "the socket has no power",
            ]
        ):
            return "no"

        # YES / POWER EXISTS
        if any(
            phrase in message
            for phrase in [
                "there is power",
                "there's power",
                "the socket works",
                "the socket is working",
                "another appliance works",
                "another appliance is working",
                "another device works",
                "another device is working",
                "the outlet works",
                "the outlet is working",
            ]
        ):
            return "yes"

        # EXACT YES
        if message in [
            "yes",
            "y",
            "yeah",
            "yep",
        ]:
            return "yes"

        # EXACT NO
        if message in [
            "no",
            "n",
            "nope",
        ]:
            return "no"

    # ==================================================
    # TRY ANOTHER SOCKET
    # ==================================================

    if step_id == "try_another_socket":

        # NOT SURE
        if any(
            phrase in message
            for phrase in [
                "not sure",
                "unsure",
                "i don't know",
                "i dont know",
                "im not sure",
                "i'm not sure",
                "i am not sure",
            ]
        ):
            return "not_sure"

        # FAN STILL DOES NOT WORK
        if any(
            phrase in message
            for phrase in [
                "the fan still doesn't work",
                "the fan still does not work",
                "it still doesn't work",
                "it still does not work",
                "the fan does not work",
                "the fan doesn't work",
                "it didn't work",
                "it did not work",
                "still not working",
                "the fan is still not working",
                "the fan is not working",
                "the fan won't work",
                "the fan wont work",
            ]
        ):
            return "no_fan_still_does_not_work"

        # FAN WORKS IN OTHER SOCKET
        if any(
            phrase in message
            for phrase in [
                "the fan works in another socket",
                "the fan works in the other socket",
                "it works in another socket",
                "it works in the other socket",
                "another socket worked",
                "the other socket worked",
                "the fan is working in another socket",
                "the fan is working in the other socket",
                "the fan works now",
                "the fan is working now",
                "yes the fan works",
                "yes, the fan works",
                "it works now",
            ]
        ):
            return "yes_fan_works"

        # EXACT YES
        if message in [
            "yes",
            "y",
            "yeah",
            "yep",
        ]:
            return "yes_fan_works"

        # EXACT NO
        if message in [
            "no",
            "n",
            "nope",
        ]:
            return "no_fan_still_does_not_work"

    # ==================================================
    # PLUG / CABLE CHECK
    # ==================================================

    if step_id == "plug_check":

        # NOT SURE
        if any(
            phrase in message
            for phrase in [
                "not sure",
                "unsure",
                "i don't know",
                "i dont know",
                "im not sure",
                "i'm not sure",
                "i am not sure",
            ]
        ):
            return "not_sure"

        # DAMAGE FOUND
        if any(
            phrase in message
            for phrase in [
                "there is damage",
                "it is damaged",
                "it's damaged",
                "the cable is damaged",
                "the plug is damaged",
                "the wire is damaged",
                "the wires are damaged",
                "there are exposed wires",
                "there is exposed wire",
                "the wire is exposed",
                "there are burn marks",
                "there is a burn mark",
                "it is burnt",
                "it's burnt",
                "it is burned",
                "it's burned",
                "it is melted",
                "it's melted",
                "the cable is cut",
                "the wire is cut",
                "the cable is broken",
                "the wire is broken",
                "the plug is broken",
            ]
        ):
            return "yes"

        # NO DAMAGE
        if any(
            phrase in message
            for phrase in [
                "no damage",
                "there is no damage",
                "there isn't any damage",
                "it is not damaged",
                "it's not damaged",
                "the cable is fine",
                "the plug is fine",
                "the wire is fine",
                "the wires are fine",
                "everything looks fine",
                "nothing looks damaged",
                "nothing is damaged",
                "no visible damage",
                "i don't see any damage",
                "i dont see any damage",
                "i do not see any damage",
            ]
        ):
            return "no"

        # EXACT YES
        if message in [
            "yes",
            "y",
            "yeah",
            "yep",
        ]:
            return "yes"

        # EXACT NO
        if message in [
            "no",
            "n",
            "nope",
        ]:
            return "no"

    # ==================================================
    # FAN RESPONSE
    # ==================================================

    if step_id == "fan_response":

        # NOTHING HAPPENS
        if any(
            phrase in message
            for phrase in [
                "nothing",
                "nothing happens",
                "no response",
                "no reaction",
                "it is completely silent",
                "it's completely silent",
                "completely silent",
                "nothing happens at all",
                "nothing happens when i switch it on",
                "nothing happens when i turn it on",
                "it does nothing",
                "it doesn't do anything",
                "it does not do anything",
            ]
        ):
            return "nothing"

        # SOUND
        if any(
            phrase in message
            for phrase in [
                "it makes a sound",
                "it makes noise",
                "i hear a sound",
                "i hear noise",
                "it hums",
                "there is a sound",
                "there is noise",
                "it makes a humming sound",
                "i hear humming",
                "it is humming",
            ]
        ):
            return "sound"

        # SIGN OF POWER
        if any(
            phrase in message
            for phrase in [
                "the light comes on",
                "the indicator comes on",
                "the indicator light comes on",
                "it shows power",
                "there is a sign of power",
                "i can see power",
                "the power light comes on",
                "the light turns on",
                "the indicator turns on",
            ]
        ):
            return "sign_of_power"

        # NOT SURE
        if any(
            phrase in message
            for phrase in [
                "not sure",
                "unsure",
                "i don't know",
                "i dont know",
                "im not sure",
                "i'm not sure",
                "i am not sure",
            ]
        ):
            return "not_sure"

    # ==================================================
    # SPEED SETTINGS
    # ==================================================

    if step_id == "speed_settings":

        # ONE SETTING WORKS
        if any(
            phrase in message
            for phrase in [
                "one setting works",
                "only one speed works",
                "one speed works",
                "only one setting works",
                "one of the speeds works",
                "one speed is working",
                "only one speed is working",
            ]
        ):
            return "one_setting_works"

        # NONE WORK
        if any(
            phrase in message
            for phrase in [
                "none work",
                "no speed works",
                "all speeds fail",
                "no setting works",
                "none of the speeds work",
                "none of the settings work",
                "all the speeds don't work",
                "all the speeds do not work",
                "no speed is working",
                "no setting is working",
            ]
        ):
            return "none_work"

        # NO SPEED SETTINGS
        if any(
            phrase in message
            for phrase in [
                "no speed settings",
                "it has no speed settings",
                "there are no speed settings",
                "it has only one speed",
                "there is only one speed",
            ]
        ):
            return "fan_has_no_speed_settings"

        # NOT SURE
        if any(
            phrase in message
            for phrase in [
                "not sure",
                "unsure",
                "i don't know",
                "i dont know",
                "im not sure",
                "i'm not sure",
                "i am not sure",
            ]
        ):
            return "not_sure"

    # ==================================================
    # VERIFICATION
    # ==================================================

    if step_id == "verification":

        # ----------------------------------------------
        # NEGATIVE ANSWERS FIRST
        # ----------------------------------------------

        if message in [
            "no",
            "n",
            "nope",
            "not yet",
        ]:
            return "no"

        if any(
            phrase in message
            for phrase in [
                "it doesn't work",
                "it does not work",
                "it still doesn't work",
                "it still does not work",
                "still not working",
                "not working",
                "it stopped working",
                "the problem is not fixed",
                "the problem isn't fixed",
                "it is not fixed",
                "it's not fixed",
                "it is still broken",
                "it's still broken",
                "the fan is still broken",
                "the fan is not working",
                "the fan doesn't work",
                "the fan does not work",
                "it isn't fixed",
                "it isnt fixed",
                "the problem remains",
            ]
        ):
            return "no"

        # ----------------------------------------------
        # POSITIVE ANSWERS
        # ----------------------------------------------

        if message in [
            "yes",
            "y",
            "yeah",
            "yep",
        ]:
            return "yes"

        if any(
            phrase in message
            for phrase in [
                "it works",
                "it's working",
                "its working",
                "it is working",
                "working normally",
                "it works normally",
                "the fan works",
                "the fan is working",
                "the fan works normally",
                "the fan is working normally",
                "the problem is fixed",
                "the problem is solved",
                "it is fixed",
                "it's fixed",
                "everything works",
                "everything is working",
                "it is working normally",
                "it's working normally",
            ]
        ):
            return "yes"

    # ==================================================
    # FALLBACK
    # ==================================================

    # If nothing matched, return the original message.
    return message