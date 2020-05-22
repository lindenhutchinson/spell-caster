# returns a list of notes formatted for a SelectField
def get_select_notes(notes, orderby):
    return [(g.id, g.title) for g in notes]