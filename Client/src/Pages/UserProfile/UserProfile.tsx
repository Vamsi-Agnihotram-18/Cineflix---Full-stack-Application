import React, { useEffect, useState } from "react";
import { useAppSelector } from "../../state/hooks";
import { BASE_URL } from "../../env";
import axios from "axios";
import { IUserData } from "../../Interfaces/userInfo.interface";
import dayjs from "dayjs";
import { CrownOutlined, DeleteOutlined } from "@ant-design/icons";
import { message } from "antd";

const UserProfile = () => {
  const userInfo = useAppSelector((state) => state.auth.userInfo);
  const [userData, setUserData] = useState<IUserData>();
  const getUserInfo = () => {
    axios
      .get(BASE_URL + "/account/user/" + userInfo.id)
      .then((res) => {
        setUserData(res.data);
      })
      .catch((e) => {
        console.log(e.message);
      });
  };
  useEffect(() => {
    getUserInfo();
  }, [userInfo]);
  useEffect(() => {
    console.log(userData, "user data");
  }, [userData]);

  const CancelTicket = (id: number) => {
    axios
      .patch(BASE_URL + "booking/ticket/cancel/" + id, {})
      .then((res) => {
        message.success("Ticket Cancelled Successfully!");
        getUserInfo();
      })
      .catch((e) => {
        console.log(e);
      });
  };

  return (
    <div className="w-full flex flex-col">
      <div className="font-semibold mb-4">User Profile</div>
      <div className="mb-5">
        <div>{userInfo.username}{userInfo.membership_type=='premium' && <CrownOutlined className="ml-2" />}</div>
        <div>{userInfo.email}</div>
        <div>{userInfo.phoneNumber}</div>
      </div>
      <div className="font-semibold mb-4">Bookings</div>
      <div className="w-full">
        {userData?.tickets.map((ticket) => {
          return (
            <div className="p-3 border-[#e0e0e0] border-[1px] w-full border-solid rounded-md mb-2">
              <div className="font-semibold mb-2 flex items-center justify-between">
                <div>{ticket.movie.name}</div>
                <div
                  className="cursor-pointer"
                  onClick={() => {
                    CancelTicket(ticket.id);
                  }}
                >
                  <DeleteOutlined />
                </div>
              </div>
              <div className=" mb-2">{ticket.theater.name}</div>
              <div className="mb-2">
                <span className="mr-2">Seats</span>
                {ticket.seats.map((seat: string) => {
                  return seat + " ";
                })}
              </div>
              <div className="mb-2">
                Timing:{" "}
                {" " + dayjs(ticket.show.show_timing).format("YYYY-MM-DD")},
                {dayjs(ticket.show.show_timing).format("h:mm A")}
              </div>
              <div>Status : {ticket.status}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default UserProfile;
