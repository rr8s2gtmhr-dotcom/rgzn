import type { RouteRecordRaw } from 'vue-router';
import type { LocalMenu } from '/@/types/api';

const componentMap: Record<string, () => Promise<any>> = {
	'/@/layout/routerView/parent.vue': () => import('/@/layout/routerView/parent.vue'),
	'/@/views/home/index.vue': () => import('/@/views/home/index.vue'),
	'/@/views/railway/relarderIndex.vue': () => import('/@/views/railway/relarderIndex.vue'),
	'/@/views/railway/detectionIndex.vue': () => import('/@/views/railway/detectionIndex.vue'),
	'/@/views/railway/maintainIndex.vue': () => import('/@/views/railway/maintainIndex.vue'),
	'/@/views/railway/deldatasIndex.vue': () => import('/@/views/railway/deldatasIndex.vue'),
	'/@/views/system/dept/index.vue': () => import('/@/views/system/dept/index.vue'),
	'/@/views/system/role/index.vue': () => import('/@/views/system/role/index.vue'),
	'/@/views/system/user/index.vue': () => import('/@/views/system/user/index.vue'),
	'/@/views/system/menu/index.vue': () => import('/@/views/system/menu/index.vue'),
	'/@/views/personal/index.vue': () => import('/@/views/personal/index.vue'),
};

export const getMenuComponent = (component: string) => componentMap[component] || componentMap['/@/layout/routerView/parent.vue'];

export const toMenuTree = (menus: LocalMenu[]): LocalMenu[] => {
	const sorted = [...menus].sort((a, b) => a.menuSort - b.menuSort);
	const build = (pid: number | null): LocalMenu[] =>
		sorted
			.filter((menu) => menu.pid === pid)
			.map((menu) => ({ ...menu, children: build(menu.id) as any }));
	return build(null);
};

export const toRouteRecords = (menus: LocalMenu[]): RouteRecordRaw[] => {
	const sorted = [...menus].sort((a, b) => a.menuSort - b.menuSort);
	const build = (pid: number | null): RouteRecordRaw[] =>
		sorted
			.filter((menu) => menu.pid === pid)
			.map((menu) => {
				const route: any = {
					path: menu.path,
					name: menu.name,
					component: getMenuComponent(menu.component),
					meta: { ...menu.meta },
				};
				if (menu.redirect) route.redirect = menu.redirect;
				const children = build(menu.id);
				if (children.length) route.children = children;
				return route;
			});
	return build(null);
};
