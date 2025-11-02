import azure.durable_functions as df

def orchestrator_function(context: df.DurableOrchestrationContext):
    result = yield context.call_activity("wait_and_work", "Simulazione lavoro")
    return result

main = df.Orchestrator.create(orchestrator_function)