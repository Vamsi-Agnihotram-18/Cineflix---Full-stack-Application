import React, { useEffect, useState } from "react";
import { BASE_URL } from "../../../env";
import axios from "axios";
import AnalyticsCharts from "./AnalyticsCharts";
//import './AnalyticsCharts.tsx'

const Analytics = () => {
  const [analytics, setAnalytics] = useState<any>();
  const getAnalytics = () => {
    axios
      .get(BASE_URL + "analytics/occupancy")
      .then((res) => {
        console.log(res.data);
        setAnalytics(res.data);
      })
      .catch((e) => {
        console.log(e);
      });
  };

  useEffect(() => {
    getAnalytics();
  }, []);

  return (
    <div>
      <AnalyticsCharts analytics={analytics}/>
      {/* <div>
        <div className="mb-3">Location vs Tickets booked analysis</div>
        <div>
          <div className="mb-2">In 30 days period</div>
          <div>
            {analytics?.locations_30_days &&
              Object.entries(analytics?.locations_30_days!).map(
                ([key, value]: any) => (
                  <div className="w-[95%]  border-solid border-[#e0e0e0] border-[1px] p-3 rounded-md bg-white mb-2">
                    {key}:{value}
                  </div>
                )
              )}
          </div>
        </div>
        <div>
          <div className="mb-2">In 60 days period</div>
          <div>
            {analytics?.locations_60_days &&
              Object.entries(analytics?.locations_60_days!).map(
                ([key, value]: any) => (
                  <div className="w-[95%]  border-solid border-[#e0e0e0] border-[1px] p-3 rounded-md bg-white mb-2">
                    {key}:{value}
                  </div>
                )
              )}
          </div>
        </div>
        <div>
          <div className="mb-2">In 90 days period</div>
          <div>
            {analytics?.locations_90_days &&
              Object.entries(analytics?.locations_90_days!).map(
                ([key, value]: any) => (
                  <div className="w-[95%]  border-solid border-[#e0e0e0] border-[1px] p-3 rounded-md bg-white mb-2">
                    {key}:{value}
                  </div>
                )
              )}
          </div>
        </div>
      </div> */}
      <div>
        <div className="mb-3">Movie vs Ticket Booked analysis</div>
        <div>
          <div className="mb-2">Past 30 days</div>
          <div>
            {analytics?.movies_30_days &&
              Object.entries(analytics?.movies_30_days!).map(
                ([key, value]: any) => (
                  <div className="w-[95%]  border-solid border-[#e0e0e0] border-[1px] p-3 rounded-md bg-white mb-2">
                    {value?.name}:{value?.occupancy}
                  </div>
                )
              )}
          </div>
        </div>
        <div>
          <div className="mb-2">Past 60 days</div>
          <div>
            {analytics?.movies_60_days &&
              Object.entries(analytics?.movies_60_days!).map(
                ([key, value]: any) => (
                  <div className="w-[95%]  border-solid border-[#e0e0e0] border-[1px] p-3 rounded-md bg-white mb-2">
                    {value?.name}:{value?.occupancy}
                  </div>
                )
              )}
          </div>
        </div>
        <div>
          <div className="mb-2">Past 90 days</div>
          <div>
            {analytics?.movies_90_days &&
              Object.entries(analytics?.movies_90_days!).map(
                ([key, value]: any) => (
                  <div className="w-[95%]  border-solid border-[#e0e0e0] border-[1px] p-3 rounded-md bg-white mb-2">
                    {value?.name}:{value?.occupancy}
                  </div>
                )
              )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
