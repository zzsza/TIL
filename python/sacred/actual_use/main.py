from experiments.random_forest import ex as rf_ex
from experiments.svc import ex as svc_ex

rf_run = rf_ex.run()
print(rf_run.config)
print(rf_run.result)
print(rf_run.info.keys())
print("New experiment run!")
rf_run2 = rf_ex.run(config_updates={"n_estimators": 10})
print(rf_run2.config)
print(rf_run2.result)

svc_run = svc_ex.run()
print(svc_run.config)
print(svc_run.result)
