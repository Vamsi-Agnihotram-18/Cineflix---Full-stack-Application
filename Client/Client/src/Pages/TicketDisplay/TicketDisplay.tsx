import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { ISeatmap } from "../../Interfaces/seatmap.interface";
import dayjs from "dayjs";
import { Button } from "antd";
import { useAppSelector } from "../../state/hooks";

const TicketDisplay = () => {
  const userInfo = useAppSelector((state) => state.auth.userInfo);
  const navigate = useNavigate();
  const location = useLocation();
  const data: { seatmapData: ISeatmap; selectedSeats: Array<string> } =
    location.state;

  useEffect(() => {
    console.log(data, "page data");
  }, [data]);

  return (
    <div>
      {" "}
      <div className="flex items-center w-full justify-center mt-10">
        <div className="flex w-[160px] h-[160px]">
          <img src={data.seatmapData.movie.image_url} alt="" />
        </div>
        <div className="w-full ml-4">
          <div className="mb-2">{data.seatmapData.movie.name}</div>
          <div className="mb-2">at {data.seatmapData.theater.name}</div>
          <div>
            Timing:{" "}
            {" " + dayjs(data.seatmapData.show_timing).format("YYYY-MM-DD")},
            {dayjs(data.seatmapData.show_timing).format("h:mm A")}
          </div>
          <div className="w-full flex items-center mt-2">
            {" "}
            <div className="mr-2 ">Selected Seats </div>
            <div>
              {data.selectedSeats.map((seat: string) => {
                return seat + " ";
              })}
            </div>
          </div>
        </div>
      </div>{" "}
      <div className="w-full mt-10 flex justify-center">
        <Button
          type="primary"
          onClick={() => {
            userInfo.role !== "guestUser"
              ? navigate("/profile")
              : navigate("/");
          }}
        >
          {userInfo.role !== "guestUser" ? (
            <span>Go to my bookings</span>
          ) : (
            <span>Book more tickets!</span>
          )}
        </Button>
      </div>
    </div>
  );
};

export default TicketDisplay;
