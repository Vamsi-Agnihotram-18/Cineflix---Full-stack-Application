import Search from "antd/es/input/Search";
import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { IMovie } from "../../Interfaces/movie.interface";
import { Card, Divider, Select } from "antd";
import Meta from "antd/es/card/Meta";
import { StarTwoTone } from "@ant-design/icons";
import { useAppSelector } from "../../state/hooks";
import { useDispatch } from "react-redux";
import axios from "axios";
import { allMovies } from "../../state/reducers/moviesReducer/moviesReducer";
import { BASE_URL } from "../../env";

const Movies = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const location = useLocation();
  const movies = useAppSelector((state: any) => state.movies);
  const [tab, setTab] = useState<string>("");
  const [filters, setFilters] = useState<any>({});

  const [tempMovies, setTempMovies] = useState<Array<IMovie>>();

  const getMovies = (params: any) => {
    let tmpParams = removeUndefined(params);
    axios
      .get(BASE_URL + "movie/movie", { params: tmpParams })
      .then((res) => {
        dispatch(allMovies(res.data.movies));
      })
      .catch((e) => {
        console.log(e);
      });
  };

  useEffect(() => {
    getMovies(filters);
  }, [filters]);

  useEffect(() => {
    console.log(movies, "movies");
    setTempMovies(movies.movies);
  }, [movies]);

  const filterMoviesByType = (movies: Array<IMovie>, targetType: string) => {
    if (targetType == "") return movies;
    return movies.filter((movie) => movie.type === targetType);
  };

  useEffect(() => {
    console.log("hash", location.hash);
    if (location.hash === "") {
      setTab("featured");
      setTempMovies(filterMoviesByType(movies.movies, ""));
    } else if (location.hash === "#now-playing") {
      setTab("now-playing");
      setTempMovies(filterMoviesByType(movies.movies, "Playing Now"));
    } else if (location.hash === "#coming-soon") {
      setTempMovies(filterMoviesByType(movies.movies, "Upcoming"));
      setTab("coming-soon");
    }
  }, [location]);

  const getFilteredMovies = (data: Array<IMovie>, searchString: string) => {
    const regex = new RegExp(searchString, "i");
    console.log(data.filter((movie) => regex.test(movie.name)));
    setTempMovies(data.filter((movie) => regex.test(movie.name)));
  };

  function removeUndefined(obj: any) {
    for (const key in obj) {
      if (obj.hasOwnProperty(key) && obj[key] === undefined) {
        delete obj[key];
      }
    }
    return obj;
  }

  return (
    <div>
      <div className="py-4 flex  items-center justify-between">
        <div className="font-semibold text-[24px]">Movies</div>

        <div className="font-semibold flex items-center">
          <span
            className={`mx-[50px] cursor-pointer hover:text-blue-400 ${
              tab === "featured" ? "text-blue-400" : ""
            }`}
            onClick={() => {
              navigate("/movies");
            }}
          >
            Featured
          </span>
          <span
            className={`mx-[50px] cursor-pointer hover:text-blue-400 ${
              tab === "now-playing" ? "text-blue-400" : ""
            }`}
            onClick={() => {
              window.location.hash = "now-playing";
            }}
          >
            Now Playing
          </span>
          <span
            className={`mx-[50px] cursor-pointer hover:text-blue-400 ${
              tab === "coming-soon" ? "text-blue-400" : ""
            }`}
            onClick={() => {
              window.location.hash = "coming-soon";
            }}
          >
            Coming Soon
          </span>
        </div>
        <div>
          <Search
            placeholder="Search for movie"
            enterButton
            onChange={(e: any) => {
              getFilteredMovies(movies.movies, e.target.value);
            }}
          />
        </div>
      </div>
      <div className="my-8 flex flex-col">
      <div className="w-[100%]   ">
          {/* <div className="font-semibold text-[18px]">Sort By</div>
          <Select
            allowClear
            className="w-full my-2"
            placeholder="Sort By"
            onChange={(e) => {
              setFilters({ ...filters, sort_by: e });
            }}
            options={[
              { value: "recent", label: "Most Recent" },
              { value: "popular", label: "Most Popular" },
              { value: "alphabetical", label: "Alphabetical Order" },
            ]}
          /> */}
          
          <div className="w-full flex justify-center items-center mb-4"> <div className="mr-3" >
          <div>Genre</div>
          <Select
            allowClear
            className="w-full my-2"
            placeholder="Select Genre"
            options={[
              { value: "action", label: "Action" },
              { value: "thriller", label: "Thriller" },
              { value: "rom_com", label: "Rom Com" },
              { value: "horror", label: "Horror" },
              { value: "feel_good", label: "Feel Good" },
            ]}
            onChange={(e) => {
              setFilters({ ...filters, genre: e });
            }}
          />
          </div>
          <div>
          <div>Rating</div>
          <Select
            allowClear
            className="w-full my-2"
            placeholder="Select Rating"
            options={[
              { value: "recent", label: "Most Recent" },
              { value: "popular", label: "Most Popular" },
              { value: "alphabetical", label: "Alphabetical Order" },
            ]}
            onChange={(e) => {
              setFilters({ ...filters, rating: e });
            }}
          />
          </div></div>
         
        </div>
        <div className="w-[100%] grid grid-cols-4 gap-4">
          {tempMovies?.map((movie: IMovie) => (
           <Card
           hoverable
           cover={<img alt="example" src={movie.image_url} style={{height: '30vh' }} />}
           onClick={() => {
             navigate(`${movie.id}`);
           }}
         >
           <Meta
             title={movie.name}
             description={
               <div className="flex justify-between">
                 <div>{movie.genre}</div>
                 <div>{movie.rating}/10</div>
               </div>
             }
           />
         </Card>
         
          ))}
        </div>

       
      </div>
    </div>
  );
};

export default Movies;
