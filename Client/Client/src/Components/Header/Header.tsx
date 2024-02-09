import {
  CrownTwoTone,
  LoginOutlined,
  LogoutOutlined,
  MailTwoTone,
  MenuOutlined,
  SettingOutlined,
  UserAddOutlined,
} from "@ant-design/icons";
import { Avatar, Button, Dropdown, Space, message } from "antd";
import type { MenuProps } from "antd";
import React, { useEffect } from "react";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import {
  setLogOut,
  setUserInfo,
} from "../../state/reducers/authReducer/authReducer";
import { useAppSelector } from "../../state/hooks";
import { ISignUp } from "../../Interfaces/signUp.interface";
import logo from "../../assets/images/logo.jpg";

const Header = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const isLoggedIn = useAppSelector((state: any) => state.auth.isLoggedIn);
  const userInfo = useAppSelector((state) => state.auth.userInfo);

  useEffect(() => {
    console.log(isLoggedIn, userInfo);
  }, [isLoggedIn, userInfo]);

  const items: MenuProps["items"] = [
    {
      label: (
        <span
          className="text-blue-600"
          onClick={() => {
            navigate("/contact");
          }}
        >
          <MailTwoTone className="mr-1" /> Contact Us
        </span>
      ),
      key: "0",
    },
    userInfo?.is_admin === true
      ? {
          label: (
            <span
              className="text-blue-600"
              onClick={() => {
                navigate("/configurations");
              }}
            >
              <SettingOutlined className="mr-1" />
              Configurations
            </span>
          ),
          key: "2",
        }
      : {
          label: (
            <span
              className="text-blue-600"
              onClick={() => {
                console.log("test");
                if (userInfo.role === "guestUser") {
                  message.warning("Signup to get user profile");
                } else {
                  navigate("/profile");
                }
              }}
            >
              <SettingOutlined className="mr-1" />
              Profile
            </span>
          ),
          key: "5",
        },
    {
      type: "divider",
    },
    {
      label: (
        <span className="text-blue-600">
          <LogoutOutlined className="mr-1" />
          Log Out
        </span>
      ),
      key: "3",
      onClick: () => {
        localStorage.clear();
        dispatch(setLogOut({}));
        dispatch(setUserInfo(null));
        navigate("/");
      },
    },
  ];
  function capitalizeFirstLetter(str: string) {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }
  return (
    <div className="py-4 bg-[#3597c4] flex justify-between items-center px-10 z-40 sticky top-0 shadow-lg">
      <div className="flex items-center justify-between w-[100%]">
        <div
          className="text-[32px] font-semibold cursor-pointer"
          onClick={() => {
            navigate("/movies");
          }}
        >
        <img width={40} height={40} src={logo} alt={"logo"} className="mr-2"/>
          MovieFlix
        </div>{" "}
    <div className="flex items-center">
        <div
          className="ml-14 mr-4 font-semibold hover:text-white cursor-pointer"
          onClick={() => {
            navigate("/movies");
          }}
        >
          Movies
        </div>
        <div
          className="mr-4 font-semibold hover:text-white cursor-pointer"
          onClick={() => {
            navigate("/theaters");
          }}
        >
          Theatres
        </div>
      <div>
        {!isLoggedIn && (
          <div className="flex items-center">
            <div
              className="mr-4 font-semibold hover:text-white cursor-pointer"
              onClick={() => {
                navigate("/signup");
              }}
            >
             Sign Up
            </div>

            <div
              className="mr-4 font-semibold hover:text-white cursor-pointer"
              onClick={() => {
                navigate("/login");
              }}
            >        
              Sign In
            </div>
          </div>
        )}
        {isLoggedIn == true && (
          <Dropdown menu={{ items }} trigger={["click"]}>
            <div className="flex items-center font-semibold cursor-pointer">
              <Avatar className="mr-1 uppercase">
                {userInfo?.username[0]}
              </Avatar>{" "}
              <span>
                Hi,&nbsp;{" "}
                <span> {capitalizeFirstLetter(userInfo.username)}</span>
              </span>
            </div>
          </Dropdown>
        )}
      </div>
      </div>
      </div>
    </div>
  );
};

export default Header;
