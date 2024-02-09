import React, { useEffect, useState } from "react";
import { useAppSelector } from "../../../state/hooks";
import { DeleteTwoTone, StarTwoTone } from "@ant-design/icons";
import { Card, FormInstance } from "antd";
import Meta from "antd/es/card/Meta";
import { IMovie } from "../../../Interfaces/movie.interface";
import axios from "axios";
import { BASE_URL } from "../../../env";
import { allMovies } from "../../../state/reducers/moviesReducer/moviesReducer";
import moment from "moment";

interface MovieConfigurations {
  showModal: (type: string) => void;
  movies: Array<IMovie>;
  getMovies: () => void;
  form: any;
  setSelectedMovie: any;
}

const Movies = ({
  showModal,
  movies,
  getMovies,
  form,
  setSelectedMovie,
}: MovieConfigurations) => {
  useEffect(() => {
    console.log(movies, "movies");
  }, [movies]);

  const DeleteMovie = (id: number) => {
    axios
      .delete(BASE_URL + "movie/movie/" + id)
      .then((res) => {
        console.log(res);
        getMovies();
      })
      .catch((e) => {
        console.log(e);
      });
  };

  return (
    <div>
      {" "}
      <div className="grid grid-cols-3 gap-4">
        {movies?.map((movie: IMovie) => {
          return (
            <Meta
              title={
                <div
                  className="flex justify-between items-center"
                  onClick={() => {
                    console.log(movie);
                    setSelectedMovie(movie);
                    form.setFieldsValue({
                      ...movie,
                      start_date: moment(movie.start_date, "YYYY-MM-DD"),
                    });
                    showModal("movies");
                  }}
                >
                  <div>
                    {movie.name.length > 25
                      ? movie.name.substring(0, 25) + "..."
                      : movie.name}
                  </div>
                  <div
                    className="cursor-pointer"
                    onClick={(e) => {
                      e.preventDefault();
                      e.stopPropagation();
                      DeleteMovie(movie.id);
                    }}
                  >
                    <DeleteTwoTone />
                  </div>
                </div>
              }
              description={
                <div className="flex items-center justify-between">
                  <span>
                    {movie.genre.length > 15
                      ? movie.genre.substring(0, 15) + "..."
                      : movie.genre}
                  </span>
                  <span>
                    <StarTwoTone className="mr-1" />
                    {movie.rating}
                  </span>
                </div>
              }
              className="bg-white p-3 rounded-md  border-solid border-[#e0e0e0] border-[1px] cursor-pointer hover:shadow-md"
            />
            // </Card>
          );
        })}
      </div>
    </div>
  );
};

export default Movies;
