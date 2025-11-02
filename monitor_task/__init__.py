import azure.functions as func
import azure.durable_functions as df

async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:

    route_params = req.route_params
    instance_id = route_params.get('instance_id')

    if not instance_id:
        return func.HttpResponse(
            body='{"status": "instance_id mancante"}',
            status_code=400,
            mimetype="application/json"
        )

    client = df.DurableOrchestrationClient(starter)

    try:
        status = await client.get_status(instance_id)
        response = {
            "status": status.runtime_status.name.lower(),
            "result": status.output,
        }
        return func.HttpResponse(
            body=f'{{"status": "{response["status"]}", "result": "{response["result"]}"}}',
            mimetype="application/json"
        )
    except Exception:
        return func.HttpResponse(
            body='{"status": "not found"}',
            status_code=404,
            mimetype="application/json"
        )