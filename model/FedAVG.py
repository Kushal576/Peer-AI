def running_model_avg(current, next, scale):
    if current == None:
        current = next
        for key in current:
            current[key] = current[key] * scale
    else:
        for key in current:
            current[key] = current[key] + (next[key] * scale)
    return current




def fed_avg_experiment(global_model, local_model,  num_clients_per_round=4):
    round_accuracy = []
    global_model.eval()
    global_model = global_model.to(cpu)
    running_avg = None

            # add local model parameters to running average
    global_model = running_model_avg(global_model, local_model.state_dict(), 1/num_clients_per_round)
        
        # set global model parameters for the next step
    # global_model.load_state_dict(running_avg)


    return global_model
