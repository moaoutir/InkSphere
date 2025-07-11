from enum import Enum

class SubscriptionType(str, Enum):
    subscribe = "subscribe"
    unsubscribe = "unsubscribe"

class PromptName(str, Enum):
    edit_blog_post = "edit_blog_post"