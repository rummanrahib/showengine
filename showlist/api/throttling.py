from rest_framework.throttling import UserRateThrottle


class CreateReviewThrottle(UserRateThrottle):
    scope = 'create-review'


class ReviewListThrottle(UserRateThrottle):
    scope = 'review-list'
