import { defineStore } from 'pinia';
import { Session } from '/@/utils/storage';
import { useAuthApi } from '/@/api/auth';

/**
 * 用户信息
 * @methods setUserInfos 设置用户信息
 */
export const useUserInfo = defineStore('userInfo', {
	state: (): UserInfosState => ({
		userInfos: {
			userName: '',
			photo: '',
			time: 0,
			roles: [],
			authBtnList: [],
		},
	}),
	actions: {
		async setUserInfos() {
			const userInfos = <UserInfos>await this.getApiUserInfo();
			this.userInfos = userInfos;
			Session.set('userInfo', userInfos);
		},
		async getApiUserInfo() {
			const res = await useAuthApi().me();
			return res.data;
		},
	},
});
