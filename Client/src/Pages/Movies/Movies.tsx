import React, { useEffect, useState, useCallback } from 'react';
import Search from "antd/es/input/Search";
import { useLocation, useNavigate } from "react-router-dom";
import { Card, Select } from "antd";
import Meta from "antd/es/card/Meta";
import { useDispatch, useSelector } from "react-redux";
import axios from "axios";
import { allMovies } from "../../state/reducers/moviesReducer/moviesReducer";
import { BASE_URL } from "../../env";
import { IMovie } from "../../Interfaces/movie.interface";
import debounce from 'lodash/debounce';

const Movies = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const dispatch = useDispatch();
  const movies = useSelector((state) => state.movies);
  const [tab, setTab] = useState('');
  const [filters, setFilters] = useState({});
  const [filteredMovies, setFilteredMovies] = useState([]);

  const getMovies = useCallback((params) => {
    axios.get(`${BASE_URL}movie/movie`, { params })
      .then(res => dispatch(allMovies(res.data.movies)))
      .catch(err => console.error(err));
  }, [dispatch]);

  useEffect(() => {
    getMovies(filters);
  }, [filters, getMovies]);

  useEffect(() => {
    const hash = location.hash;
    setTab(hash.replace('#', '') || 'featured');
  }, [location]);

  useEffect(() => {
    const filtered = movies.movies.filter(movie => {
      if (!tab || tab === 'featured') return true;
      return movie.type === tab;
    });
    setFilteredMovies(filtered);
  }, [movies, tab]);

  const handleSearch = debounce((searchString) => {
    const regex = new RegExp(searchString, 'i');
    setFilteredMovies(movies.movies.filter(movie => regex.test(movie.name)));
  }, 300);

  const handleChangeTab = (newTab) => {
    navigate(`/movies#${newTab}`);
  };

  return (
    <div>
      {/* ... Tab and Search Components ... */}
      <div className="my-8">
        <div className="w-full flex justify-center items-center mb-4">
          {/* Genre and Rating Selects */}
        </div>
        <div className="grid grid-cols-4 gap-4">
          {filteredMovies.map(movie => (
            <Card
              key={movie.id}
              hoverable
              cover={<img alt={movie.name} src={movie.image_url} style={{ height: '30vh' }} />}
              onClick={() => navigate(`/movie/${movie.id}`)}
            >
              <Meta
                title={movie.name}
                description={(
                  <div className="flex justify-between">
                    <div>{movie.genre}</div>
                    <div>{movie.rating}/10</div>
                  </div>
                )}
              />
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Movies;