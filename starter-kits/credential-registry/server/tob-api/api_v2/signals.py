from haystack.signals import RealtimeSignalProcessor
from api_v2.models.CredentialSet import CredentialSet

class RelatedRealtimeSignalProcessor(RealtimeSignalProcessor):
    reindex_related = True

    """
    Extension to haystack's RealtimeSignalProcessor not only causing the
    search_index to update on saved model, but also for image url, which is
    needed to show images on search results.

    Models must define a reindex_related list which defines which relationships
    to traverse during indexing

    adapted from:
    https://stackoverflow.com/questions/27635340/update-django-haystack-search-index-for-prepared-field#27753826
    """

    def check_if_reindex(self, instance):
        if type(instance) is CredentialSet:
            # don't re-index if it's a "foundational" type
            if instance.topic.type == instance.credential_type.description:
                return False

            # don't re-index if we already have this cred type on our topic
            topic_credential_sets = instance.topic.credential_sets.all()
            for topic_credential_set in topic_credential_sets:
                if topic_credential_set.id != instance.id and topic_credential_set.credential_type == instance.credential_type:
                    return False

        # default return True
        return True

    def handle_save(self, sender, instance, **kwargs):
        if self.reindex_related and hasattr(instance, "reindex_related"):
            if self.check_if_reindex(instance):
                for related in instance.reindex_related:
                    related_obj = getattr(instance, related)
                    related_objs = None

                    # Possible that the relationship is one or many.
                    # Handle both.
                    try:
                        related_objs = related_obj.all()
                    except AttributeError:
                        pass

                    if related_objs:
                        for related_obj in related_objs:
                            self.handle_save(related_obj.__class__, related_obj)
                    else:
                        self.handle_save(related_obj.__class__, related_obj)
        return super(RelatedRealtimeSignalProcessor, self).handle_save(
            sender, instance, **kwargs
        )

    def handle_delete(self, sender, instance, **kwargs):
        if self.reindex_related and hasattr(instance, "reindex_related"):
            for related in instance.reindex_related:
                related_obj = getattr(instance, related)
                related_objs = None
                try:
                    related_objs = related_obj.all()
                except AttributeError:
                    pass

                if related_objs:
                    for related_obj in related_objs:
                        self.handle_delete(related_obj.__class__, related_obj)
                else:
                    self.handle_delete(related_obj.__class__, related_obj)
        return super(RelatedRealtimeSignalProcessor, self).handle_delete(
            sender, instance, **kwargs
        )
