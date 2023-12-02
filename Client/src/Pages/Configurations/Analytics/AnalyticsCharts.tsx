import React from 'react';
import { Pie, Bar } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

const AnalyticsCharts = (props: { analytics: any; }) => {
    const analytics = props.analytics;
  const pieData = {
    labels: analytics ? Object.keys(analytics.locations_30_days) : [],
    datasets: [{
      label: 'Location Occupancy in 30 days',
      data: analytics ? Object.values(analytics.locations_30_days) : [],
      backgroundColor: [
        // array of colors for each segment
      ],
      borderWidth: 1,
    }],
  };


  const pieData2 = {
    labels: analytics ? Object.keys(analytics.locations_60_days) : [],
    datasets: [{
      label: 'Location Occupancy in 30 days',
      data: analytics ? Object.values(analytics.locations_60_days) : [],
      backgroundColor: [
        // array of colors for each segment
      ],
      borderWidth: 1,
    }],
  };

  const pieData3 = {
    labels: analytics ? Object.keys(analytics.locations_90_days) : [],
    datasets: [{
      label: 'Location Occupancy in 30 days',
      data: analytics ? Object.values(analytics.locations_90_days) : [],
      backgroundColor: [
        // array of colors for each segment
      ],
      borderWidth: 1,
    }],
  };


// const pieData4 = {
//     labels: analytics ? Object.keys(analytics.movies_30_days) : [],
//     datasets: [{
//         label: 'Movies in 30 days',
//         data: analytics ? Object.values(analytics.movies_30_days).map((movie: { occupancy: any }) => movie.occupancy) : [],
//         backgroundColor: [
//           // array of colors for each segment
//         ],
//         borderWidth: 1,
//       }],
  //    
//};

// const pieData5 = {
//     labels: analytics ? Object.keys(analytics.movies_60_days) : [],
//     datasets: [{
//       label: 'Movies in 60 days',
//       data: analytics ? Object.values(analytics.movies_60_days) : [],
//       backgroundColor: [
//         // array of colors for each segment
//       ],
//       borderWidth: 1,
//     }],
// };

// const pieData6 = {
//     labels: analytics ? Object.keys(analytics.movies_90_days) : [],
//     datasets: [{
//       label: 'Movies in 90 days',
//       data: analytics ? Object.values(analytics.movies_90_days) : [],
//       backgroundColor: [
//         // array of colors for each segment
//       ],
//       borderWidth: 1,
//     }],
 //};


//  const movies_30_days = Array.isArray(analytics?.movies_30_days) ? analytics.movies_30_days : [];

  return (
    <div>
      <div>
        <h3>Location Occupancy in 30 Days (Pie Chart)</h3>
        <div style={{ width: '300px', height: '300px' }}>
        <Pie data={pieData} />
        </div>
      </div>
     

      <div>
        <h3>Location Occupancy in 60 Days (Pie Chart)</h3>
        <div style={{ width: '300px', height: '300px' }}>
        <Pie data={pieData2} />
        </div>
      </div>


      <div>
        <h3>Location Occupancy in 90 Days (Pie Chart)</h3>
        <div style={{ width: '300px', height: '300px' }}>
        <Pie data={pieData3} />
        </div>
      </div>

      {/* <div>
        <h3>Movies in 30 Days (Pie Chart)</h3>
        <div style={{ width: '300px', height: '300px' }}>
        <Pie data={pieData4} />
        </div>
      </div> */}

    </div>
  );
}

export default AnalyticsCharts;
