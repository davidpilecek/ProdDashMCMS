def read_tag_value(cc, hc, tag_name):

    tag_id = cc.get_tags_by_name([tag_name])[0]["id"]
    return hc.get_tag_values(tag_id)[0]["value"]

def read_tag_string(cc, hc, tag_name):

    tag_id = cc.get_tags_by_name([tag_name])[0]["id"]
    return hc.get_tag_values(tag_id)[0]["valueString"]

def write_tag_value(cc, hc, tag_name, value, timestamp):
    tag_id = cc.get_tags_by_name([tag_name])[0]["id"]
    payload = [
        {
          "tagID": tag_id,
          "timestamp": timestamp,
          "value": value,
        "quality":192
        }]
    hc.post_tag_values(payload)

def write_tag_string(cc, hc, tag_name, value, timestamp):
    tag_id = cc.get_tags_by_name([tag_name])[0]["id"]
    payload = [
        {
          "tagID": tag_id,
          "timestamp": timestamp,
          "valueString": value,
        "quality":192
        }]
    hc.post_tag_values(payload)