import {
  FETCH_GOODS_LIST_SUCCESS, FETCH_GOODS_LIST_FAILURE, FETCH_GOODS_LIST_ERROR,
  FETCH_BANNER_LIST_SUCCESS, FETCH_BANNER_LIST_FAILURE, FETCH_BANNER_LIST_ERROR,
  FETCH_MSG_LIST_SUCCESS, FETCH_MSG_LIST_FAILURE, FETCH_MSG_LIST_ERROR
} from './actions'


// ------------------------------------
// Reducer
// ------------------------------------

function goodsListReducer(state = [], action) {
  switch (action.type) {
    case FETCH_GOODS_LIST_SUCCESS:
      return [...state, ...action.goodsList]
    case FETCH_GOODS_LIST_FAILURE:
    case FETCH_GOODS_LIST_ERROR:
    default:
      return state
  }
}

function bannerListReducer(state = [], action) {
  switch (action.type) {
    case FETCH_BANNER_LIST_SUCCESS:
      return [...state, ...action.bannerList]
    case FETCH_BANNER_LIST_FAILURE:
    case FETCH_BANNER_LIST_ERROR:
    default:
      return state
  }
}

function msgListReducer(state = [], action) {
  switch (action.type) {
    case FETCH_MSG_LIST_SUCCESS:
      return [...state, ...action.msgList]
    case FETCH_MSG_LIST_FAILURE:
    case FETCH_MSG_LIST_ERROR:
    default:
      return state
  }
}

const initialState = {}
export default function homeReducer(state = initialState, action) {
  console.log('homeReducer...')
  switch (action.type) {
    case FETCH_GOODS_LIST_SUCCESS:
    case FETCH_GOODS_LIST_FAILURE:
    case FETCH_GOODS_LIST_ERROR:
      return {
        ...state,
        goodsList: goodsListReducer(state.goodsList = [], action)
      }

    case FETCH_BANNER_LIST_SUCCESS:
    case FETCH_BANNER_LIST_FAILURE:
    case FETCH_BANNER_LIST_ERROR:
      return {
        ...state,
        bannerList: bannerListReducer(state.bannerList = [], action)
      }

    case FETCH_MSG_LIST_SUCCESS:
    case FETCH_MSG_LIST_FAILURE:
    case FETCH_MSG_LIST_ERROR:
      return {
        ...state,
        msgList: msgListReducer(state.msgList = [], action)
      }
    default:
      return state
  }


}
