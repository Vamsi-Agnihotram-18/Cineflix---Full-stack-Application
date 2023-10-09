import React, { useEffect, useState, useMemo } from 'react';

interface AnalyticsData {
  movieId: number;
  location: string;
  date: string;
  bookings: number;
}

// Utility Functions
const filterByDateRange = (data: AnalyticsData[], days: number) => {
  // ... existing logic
};

const groupData = (data: AnalyticsData[]) => {
  // ... existing logic
};

// Presentation Component for Grouped Data
const GroupedAnalytics = ({ data }: { data: ReturnType<typeof groupData> }) => {
  return (
    <ul>
      {Object.keys(data).map((location) => (
        <li key={location}>
          <h3>{location}</h3>
          <ul>
            {Object.entries(data[location]).map(([movie, bookings]) => (
              <li key={movie}>
                {movie}: {bookings} bookings
              </li>
            ))}
          </ul>
        </li>
      ))}
    </ul>
  );
};

const Analytics: React.FC = () => {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    // Fetch data asynchronously from the API
    const fetchData = async () => {
      setIsLoading(true);
      try {
        // Replace this with actual API call
        const response = await fetch('/analytics');
        const data: AnalyticsData[] = await response.json();
        setAnalyticsData(data);
      } catch (err) {
        setError('Failed to fetch data');
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  const renderAnalytics = (days: number) => {
    const filteredData = useMemo(() => filterByDateRange(analyticsData, days), [analyticsData, days]);
    const groupedData = useMemo(() => groupData(filteredData), [filteredData]);

    return (
      <div>
        <h2>Analytics for {days} Days</h2>
        <GroupedAnalytics data={groupedData} />
      </div>
    );
  };

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      {renderAnalytics(30)}
      {renderAnalytics(60)}
      {renderAnalytics(90)}
    </div>
  );
};

export default Analytics;
