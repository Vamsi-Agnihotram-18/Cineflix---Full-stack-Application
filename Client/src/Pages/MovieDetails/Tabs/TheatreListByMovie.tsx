import React, { useMemo } from 'react';
import { Card, Button } from 'antd';
import { useNavigate } from 'react-router-dom';
import dayjs from 'dayjs';
import { ITheater } from '../../../Interfaces/theater.interface';

export interface TheatreListByMovieProps {
  date: string;
  theaters: Array<{
    theater: ITheater;
    shows: Array<{ id: number; show_timing: string }>;
  }>;
}

const TheatreListByMovie: React.FC<TheatreListByMovieProps> = ({ date, theaters }) => {
  const navigate = useNavigate();

  const formattedTheaters = useMemo(() => theaters.map(theater => ({
    ...theater,
    theaterName: theater.theater.name.length > 30 ? `${theater.theater.name.substring(0, 30)}...` : theater.theater.name
  })), [theaters]);

  return (
    <div className="pt-10 w-[80%] grid grid-cols-2 gap-6">
      {formattedTheaters.map((theater) => (
        <Card
          key={theater.theater.id}
          title={<span className="font-bold">{theater.theaterName}</span>}
          style={{ minWidth: 300 }}
          className="cursor-pointer"
        >
          <div>{theater.theater.short_address}</div>
          <div className="flex flex-wrap gap-3 pt-8">
            {theater.shows.map((show) => (
              <Button
                key={show.id}
                onClick={() => navigate(`/seatmap/${show.id}`)}
              >
                {dayjs(show.show_timing).format("h:mm A")}
              </Button>
            ))}
          </div>
        </Card>
      ))}
    </div>
  );
};

export default TheatreListByMovie;