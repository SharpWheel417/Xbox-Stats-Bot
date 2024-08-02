class Achievement:
  def __init__(self, name, progressState, isSecret, description, lockedDescription, value, iconURL):
    self.name = name
    self.progressState = progressState
    self.isSecret = isSecret
    self.description = description
    self.lockedDescription = lockedDescription
    self.value = value
    self.iconURL = iconURL