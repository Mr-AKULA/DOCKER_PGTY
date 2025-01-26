from(bucket: "eee")
  |> range(start: 2024-04-18T00:00:00Z, stop: 2024-04-18T00:02:00Z)
  |> filter(fn: (r) => r["_measurement"] == "sensors_data_prediction")
  |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
