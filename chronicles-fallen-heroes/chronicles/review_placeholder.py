class ReviewStatus:
	def __init__(self):
		self.reviewed = False
		self.review_date = None

	def mark_reviewed(self, date):
		self.reviewed = True
		self.review_date = date

	def is_ready_for_purchase(self, current_date):
		if not self.reviewed or not self.review_date:
			return False
		delta = (current_date - self.review_date).days
		return delta <= 7
