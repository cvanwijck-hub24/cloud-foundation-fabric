from google.api.metric_pb2 import MetricDescriptor
from google.cloud import monitoring_v3
from http import HTTPStatus
import logging

LOGGER = logging.getLogger('utility')

client = monitoring_v3.MetricServiceClient()


def get_custom_metric(project: str, key: str) -> MetricDescriptor:
    """Gets a custom metric from Cloud Monitoring.

    Args:
        project: The GCP project ID.
        key: The key of the custom metric.

    Returns:
        A ga_metric.MetricDescriptor object representing the custom metric, or None if the metric does not exist.
    """

    metric_name = f"projects/{project}/metricDescriptors/{key}"

    request = monitoring_v3.GetMetricDescriptorRequest(
          name=metric_name,
    )

    try:
        response = client.get_metric_descriptor(request=request)
    except Exception as e:
        if e.code == HTTPStatus.NOT_FOUND:
            return None
        else:
            LOGGER.error(f"Unexpected {e=}, {type(e)=}")
            raise
    return response


def create_custom_metric(project: str, descriptor: MetricDescriptor) -> MetricDescriptor:
    """Creates a new custom metric in Cloud Monitoring.

    Args:
      project: GCP project id
      descriptor: A description of the custom metric to create.

    Returns:
      The newly created custom metric.
    """

    project_name = f"projects/{project}"

    try:
        descriptor = client.create_metric_descriptor(
              name=project_name, metric_descriptor=descriptor
        )
    except Exception as e:
        LOGGER.error(f"Unexpected {e=}, {type(e)=}")
        return None

    LOGGER.info("Created {}.".format(descriptor.name))
    return descriptor
