import request from '/@/utils/request';

export type ResourceKey = 'menus' | 'units' | 'roles' | 'users' | 'relarders' | 'detections' | 'maintains' | 'deldatas';

export interface PageQuery {
	pageNum?: number;
	pageSize?: number;
	keyword?: string;
	[key: string]: any;
}

export interface PageResult<T = any> {
	list: T[];
	total: number;
	pageNum: number;
	pageSize: number;
}

export function useResourceApi() {
	return {
		list: (resource: ResourceKey) => request({ url: `/${resource}`, method: 'get' }),
		page: (resource: ResourceKey, params: PageQuery) => request({ url: `/${resource}/page`, method: 'get', params }),
		get: (resource: ResourceKey, id: number) => request({ url: `/${resource}/${id}`, method: 'get' }),
		create: (resource: ResourceKey, data: any) => request({ url: `/${resource}`, method: 'post', data }),
		update: (resource: ResourceKey, id: number, data: any) => request({ url: `/${resource}/${id}`, method: 'put', data }),
		remove: (resource: ResourceKey, id: number) => request({ url: `/${resource}/${id}`, method: 'delete' }),
	};
}
