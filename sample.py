import datetime
from azure.mgmt.monitor import MonitorManagementClient
resource_id = (
    "subscriptions/{}/"
    "resourceGroups/{}/"
    "providers/Microsoft.Compute/virtualMachines/{}"
).format(subscription_id, resource_group_name, vm_name)

# create client
client = MonitorManagementClient(
    credentials,
    subscription_id
)

# You can get the available metrics of this specific resource
for metric in client.metric_definitions.list(resource_id):
    # azure.monitor.models.MetricDefinition
    print("{}: id={}, unit={}".format(
        metric.name.localized_value,
        metric.name.value,
        metric.unit
    ))

# Get CPU total of yesterday for this VM, by hour

today = datetime.datetime.now().date()
lastmonth = today - datetime.timedelta(days=31)

metrics_data = client.metrics.list(
    resource_id,
    timespan="{}/{}".format(lastmonth, today),
    interval='PT1H',
    metricnames='Percentage CPU',
    aggregation='Total'
)

for item in metrics_data.value:
    print("{} ({})".format(item.name.localized_value, item.unit.name))
    for timeserie in item.timeseries:
        for data in timeserie.data:
            # azure.mgmt.monitor.models.MetricData
            print("{}: {}".format(data.time_stamp, data.total))



# email
from azure.mgmt.monitor.models import RuleEmailAction
rule_action = RuleEmailAction(
    send_to_service_owners = True,
    custom_emails = [
        'monitoringemail@microsoft.com'
    ]
)
