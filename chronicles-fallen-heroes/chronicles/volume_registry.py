if __name__ == "__main__":
	registry = VolumeRegistry()
	registry.add_volume("Chronicles of the Fallen Heroes", 2025, "VolumeGuardian")
	registry.add_volume("Chronicles: Rise of the Kin", 2026, "LegacyReader")
	print("Volumes:", registry.list_volumes())
	print("Badge for 'Chronicles of the Fallen Heroes':", registry.get_badge_for_volume("Chronicles of the Fallen Heroes"))
class VolumeRegistry:
	def __init__(self):
		self.volumes = []

	def add_volume(self, title, release_year, badge_required):
		self.volumes.append({
			"title": title,
			"release_year": release_year,
			"badge_required": badge_required
		})

	def list_volumes(self):
		return [v["title"] for v in self.volumes]

	def get_badge_for_volume(self, title):
		for v in self.volumes:
			if v["title"] == title:
				return v["badge_required"]
		return None


if __name__ == "__main__":
	registry = VolumeRegistry()
	registry.add_volume("Chronicles of the Fallen Heroes", 2025, "VolumeGuardian")
	registry.add_volume("Chronicles: Rise of the Kin", 2026, "LegacyReader")
	print("Volumes:", registry.list_volumes())
	print("Badge for 'Chronicles of the Fallen Heroes':", registry.get_badge_for_volume("Chronicles of the Fallen Heroes"))
