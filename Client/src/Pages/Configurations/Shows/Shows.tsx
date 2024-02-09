import React, { useCallback } from 'react';
import { IShow } from '../../../Interfaces/show.interface';
import dayjs from 'dayjs';
import axios from 'axios';
import { BASE_URL } from '../../../env';
import { DeleteTwoTone } from '@ant-design/icons';
import { message } from 'antd';

export interface IShowInterface {
  showModal: (type: string) => void;
  shows: Array<IShow>;
  getShows: () => void;
  form: any; // Consider using a more specific type
  setSelectedShow: (show: IShow) => void;
}
const Shows: React.FC<IShowInterface> = ({
  showModal,
  shows,
  getShows,
  form,
  setSelectedShow,
}) => {
  const deleteShow = useCallback((id: number, event: React.MouseEvent) => {
    event.stopPropagation();
    axios
      .delete(`${BASE_URL}shows/show/${id}`)
      .then(() => {
        message.success('Show deleted successfully');
        getShows();
      })
      .catch(() => {
        message.error('Failed to delete show');
      });
  }, [getShows]);

  const handleShowClick = useCallback((show: IShow) => {
    setSelectedShow(show);
    form.setFieldsValue(show);
    // showModal('shows'); // Uncomment if needed
  }, [form, setSelectedShow]);

  return (
    <div>
      {shows.map((show) => (
        <div
          key={show.id}
          className="w-[95%] border-[1px] border-solid border-[#e0e0e0] p-3 mb-2 rounded-md flex justify-between items-center"
          onClick={() => handleShowClick(show)}
        >
          <div>
            <div>Movie: {show.movie.name}</div>
            <div>Theater: {show.theater.name}</div>
            <div>Show Timing: {dayjs(show.show_timing).format('dddd, MMMM DD, YYYY, h:mm A')}</div>
          </div>
          <DeleteTwoTone
            className="cursor-pointer"
            onClick={(event) => deleteShow(show.id, event)}
          />
        </div>
      ))}
    </div>
  );
};

export default Shows;
