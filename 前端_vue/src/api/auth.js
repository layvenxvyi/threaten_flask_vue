import axios from 'axios'
import Qs from 'qs'
import {baseUrl} from './config'

export const getDetailInfo = (page,select_origin,select_type,select_shotkey) => {
  return axios({
    method: 'post',
    url: baseUrl,
    // headers: {
    //   'Content-Type': 'application/x-www-form-urlencoded'
    // },
    data: Qs.stringify({
      "page": page,
      "select_origin":select_origin,
      "select_type":select_type,
      "select_shotkey":select_shotkey,
    })
  });
};
export default {
  getDetailInfo,
}
