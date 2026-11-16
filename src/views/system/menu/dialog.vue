<template>
	<div class="system-menu-dialog-container">
		<el-dialog :title="state.dialog.title" v-model="state.dialog.isShowDialog" width="769px">
			<el-form ref="menuDialogFormRef" :model="state.ruleForm" size="default" label-width="80px">
				<el-row :gutter="35">
					<el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
						<el-form-item label="上级菜单">
							<el-cascader
								:options="state.menuData"
								:props="{ checkStrictly: true, value: 'path', label: 'title', children: 'children' }"
								placeholder="请选择上级菜单"
								clearable
								class="w100"
								v-model="state.ruleForm.menuSuperior"
							>
								<template #default="{ node, data }">
									<span>{{ data.title }}</span>
									<span v-if="!node.isLeaf"> ({{ data.children.length }}) </span>
								</template>
							</el-cascader>
						</el-form-item>
					</el-col>
					<el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
						<el-form-item label="菜单类型">
							<el-radio-group v-model="state.ruleForm.menuType">
								<el-radio label="menu">菜单</el-radio>
								<el-radio label="btn">按钮</el-radio>
							</el-radio-group>
						</el-form-item>
					</el-col>
					<el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
						<el-form-item label="菜单名称">
							<el-input v-model="state.ruleForm.meta.title" placeholder="格式：message.router.xxx" clearable />
						</el-form-item>
					</el-col>
					<template v-if="state.ruleForm.menuType === 'menu'">
						<el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
							<el-form-item label="路由名称">
								<el-input v-model="state.ruleForm.name" placeholder="路由中的 name 值" clearable />
							</el-form-item>
						</el-col>
						<el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
							<el-form-item label="路由路径">
								<el-input v-model="state.ruleForm.path" placeholder="路由中的 path 值" clearable />
							</el-form-item>
						</el-col>
						<el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
							<el-form-item label="重定向">
								<el-input v-model="state.ruleForm.redirect" placeholder="请输入路由重定向" clearable />
							</el-form-item>
						</el-col>
						<el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
							<el-form-item label="菜单图标">
								<IconSelector placeholder="请输入菜单图标" v-model="state.ruleForm.meta.icon" />
							</el-form-item>
						</el-col>
						<el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
							<el-form-item label="组件路径">
								<el-select v-model="state.ruleForm.componentAlias" placeholder="组件路径" clearable class="w100">
									<el-option v-for="item in componentOptions" :key="item" :label="item" :value="item" />
								</el-select>
							</el-form-item>
						</el-col>
						<el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
							<el-form-item label="权限标识">
								<el-select v-model="state.ruleForm.meta.roles" multiple placeholder="取角色管理" clearable class="w100">
									<el-option label="admin" value="admin" />
									<el-option label="common" value="common" />
								</el-select>
							</el-form-item>
						</el-col>
					</template>
					<template v-if="state.ruleForm.menuType === 'btn'">
						<el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
							<el-form-item label="权限标识">
								<el-input v-model="state.ruleForm.btnPower" placeholder="请输入权限标识" clearable />
							</el-form-item>
						</el-col>
					</template>
					<el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
						<el-form-item label="菜单排序">
							<el-input-number v-model="state.ruleForm.menuSort" controls-position="right" placeholder="请输入排序" class="w100" />
						</el-form-item>
					</el-col>
				</el-row>
			</el-form>
			<template #footer>
				<span class="dialog-footer">
					<el-button @click="onCancel" size="default">取 消</el-button>
					<el-button type="primary" @click="onSubmit" size="default">{{ state.dialog.submitTxt }}</el-button>
				</span>
			</template>
		</el-dialog>
	</div>
</template>

<script setup lang="ts" name="systemMenuDialog">
import { defineAsyncComponent, reactive, ref } from 'vue';
import { ElMessage } from 'element-plus';
import { useResourceApi } from '/@/api/resource';
import { i18n } from '/@/i18n/index';
import { toMenuTree } from '/@/utils/menuHelper';
import type { LocalMenu } from '/@/types/api';
import { refreshFrontEndRoutes } from '/@/router/frontEnd';

const emit = defineEmits(['refresh']);
const IconSelector = defineAsyncComponent(() => import('/@/components/iconSelector/index.vue'));

const api = useResourceApi();
let cachedMenus: LocalMenu[] = [];
const loadMenus = async (): Promise<LocalMenu[]> => {
	const res = await api.list('menus');
	cachedMenus = (res.data as LocalMenu[]) || [];
	return cachedMenus;
};
const menuDialogFormRef = ref();
const componentOptions = [
	'/@/layout/routerView/parent.vue',
	'/@/views/home/index.vue',
	'/@/views/railway/relarderIndex.vue',
	'/@/views/railway/detectionIndex.vue',
	'/@/views/railway/maintainIndex.vue',
	'/@/views/railway/deldatasIndex.vue',
	'/@/views/system/dept/index.vue',
	'/@/views/system/role/index.vue',
	'/@/views/system/user/index.vue',
	'/@/views/system/menu/index.vue',
	'/@/views/personal/index.vue',
];

const defaultForm = () => ({
	id: undefined as number | undefined,
	menuSuperior: [] as string[],
	menuType: 'menu' as 'menu' | 'btn',
	name: '',
	component: '',
	componentAlias: '',
	isLink: false,
	menuSort: 0,
	path: '',
	redirect: '',
	meta: {
		title: '',
		icon: '',
		isHide: false,
		isKeepAlive: true,
		isAffix: false,
		isLink: '',
		isIframe: false,
		roles: [] as string[],
	},
	btnPower: '',
});

const state = reactive({
	ruleForm: defaultForm(),
	menuData: [] as any[],
	dialog: { isShowDialog: false, type: '', title: '', submitTxt: '' },
});

const getMenuData = (menus: LocalMenu[]): any[] =>
	toMenuTree(menus).map((menu) => ({
		...menu,
		title: i18n.global.t(menu.meta.title),
		children: getMenuData((menu.children || []) as LocalMenu[]),
	}));

const getParentPaths = (pid: number | null, menus: LocalMenu[]): string[] => {
	const result: string[] = [];
	let current = menus.find((menu) => menu.id === pid);
	while (current) {
		result.unshift(current.path);
		current = menus.find((menu) => menu.id === current?.pid);
	}
	return result;
};

const openDialog = async (type: string, row?: LocalMenu) => {
	const menus = await loadMenus();
	state.menuData = getMenuData(menus);
	if (type === 'edit' && row) {
		state.ruleForm = JSON.parse(JSON.stringify(row));
		state.ruleForm.menuSuperior = getParentPaths(row.pid, menus);
		state.ruleForm.componentAlias = row.component;
		state.dialog = { isShowDialog: true, type: 'edit', title: '修改菜单', submitTxt: '修 改' };
	} else {
		state.ruleForm = defaultForm();
		state.ruleForm.menuSuperior = row ? getParentPaths(row.id, menus) : [];
		state.dialog = { isShowDialog: true, type: 'add', title: '新增菜单', submitTxt: '新 增' };
	}
};

const closeDialog = () => (state.dialog.isShowDialog = false);
const onCancel = () => closeDialog();
const onSelectIframeChange = () => {
	state.ruleForm.isLink = state.ruleForm.meta.isIframe;
};

const onSubmit = async () => {
	const form = state.ruleForm;
	const menus = await loadMenus();
	const parentPath = form.menuSuperior.length ? form.menuSuperior[form.menuSuperior.length - 1] : '';
	const parent = menus.find((menu) => menu.path === parentPath);
	const item: Omit<LocalMenu, 'id'> & { id?: number } = {
		id: form.id || undefined,
		pid: parent ? parent.id : null,
		path: form.path,
		name: form.name,
		component: form.componentAlias || '/@/layout/routerView/parent.vue',
		redirect: form.redirect || undefined,
		menuType: form.menuType,
		menuSort: form.menuSort,
		btnPower: form.btnPower || undefined,
		meta: { ...form.meta, roles: Array.isArray(form.meta.roles) ? form.meta.roles : [] },
	};
	if (form.id) {
		await api.update('menus', form.id, item);
		ElMessage.success('修改成功');
	} else {
		await api.create('menus', item);
		ElMessage.success('新增成功');
	}
	await refreshFrontEndRoutes();
	closeDialog();
	emit('refresh');
};

defineExpose({ openDialog });
</script>
