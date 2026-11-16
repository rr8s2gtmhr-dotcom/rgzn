<template>
	<div class="system-menu-container layout-pd">
		<el-card shadow="hover">
			<div class="system-menu-search mb15">
				<el-input v-model="state.search" size="default" placeholder="请输入菜单名称" style="max-width: 180px" clearable />
				<el-button size="default" type="primary" class="ml10" @click="getTableData">
					<el-icon><ele-Search /></el-icon>
					查询
				</el-button>
				<el-button size="default" type="success" class="ml10" @click="onOpenAddMenu">
					<el-icon><ele-FolderAdd /></el-icon>
					新增菜单
				</el-button>
			</div>
			<el-table
				:data="state.tableData.data"
				v-loading="state.tableData.loading"
				style="width: 100%"
				row-key="id"
				default-expand-all
				:tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
			>
				<el-table-column label="菜单名称" show-overflow-tooltip>
					<template #default="scope">
						<SvgIcon :name="scope.row.meta.icon" />
						<span class="ml10">{{ $t(scope.row.meta.title) }}</span>
					</template>
				</el-table-column>
				<el-table-column prop="path" label="路由路径" show-overflow-tooltip />
				<el-table-column prop="component" label="组件路径" show-overflow-tooltip />
				<el-table-column label="权限标识" show-overflow-tooltip>
					<template #default="scope">
						<span>{{ scope.row.meta.roles }}</span>
					</template>
				</el-table-column>
				<el-table-column prop="menuSort" label="排序" show-overflow-tooltip width="80" />
				<el-table-column label="类型" show-overflow-tooltip width="80">
					<template #default="scope">
						<el-tag type="success" size="small">{{ scope.row.menuType === 'btn' ? '按钮' : '菜单' }}</el-tag>
					</template>
				</el-table-column>
				<el-table-column label="操作" show-overflow-tooltip width="160">
					<template #default="scope">
						<el-button size="small" text type="primary" @click="onOpenAddMenu(scope.row)">新增</el-button>
						<el-button size="small" text type="primary" @click="onOpenEditMenu('edit', scope.row)">修改</el-button>
						<el-button size="small" text type="primary" @click="onTabelRowDel(scope.row)">删除</el-button>
					</template>
				</el-table-column>
			</el-table>
		</el-card>
		<MenuDialog ref="menuDialogRef" @refresh="getTableData" />
	</div>
</template>

<script setup lang="ts" name="systemMenu">
import { defineAsyncComponent, ref, onMounted, reactive } from 'vue';
import { ElMessageBox, ElMessage } from 'element-plus';
import { useResourceApi } from '/@/api/resource';
import { i18n } from '/@/i18n/index';
import { toMenuTree } from '/@/utils/menuHelper';
import type { LocalMenu } from '/@/types/api';
import { refreshFrontEndRoutes } from '/@/router/frontEnd';

const MenuDialog = defineAsyncComponent(() => import('/@/views/system/menu/dialog.vue'));

const api = useResourceApi();
const menuDialogRef = ref();
const state = reactive({
	search: '',
	tableData: {
		data: [] as LocalMenu[],
		loading: true,
	},
});

const getTableData = async () => {
	state.tableData.loading = true;
	try {
		const res = await api.list('menus');
		let menus = (res.data as LocalMenu[]) || [];
		const keyword = state.search.trim().toLowerCase();
		if (keyword) {
			menus = menus.filter(
				(menu) => i18n.global.t(menu.meta.title).toLowerCase().includes(keyword) || menu.path.toLowerCase().includes(keyword)
			);
		}
		state.tableData.data = toMenuTree(menus);
	} finally {
		state.tableData.loading = false;
	}
};
const onOpenAddMenu = (row?: LocalMenu) => {
	menuDialogRef.value.openDialog('add', row);
};
const onOpenEditMenu = (type: string, row: LocalMenu) => {
	menuDialogRef.value.openDialog(type, row);
};
const collectIds = (menu: LocalMenu): number[] => [menu.id, ...(menu.children || []).flatMap(collectIds)];
const onTabelRowDel = (row: LocalMenu) => {
	ElMessageBox.confirm(`此操作将永久删除菜单：${i18n.global.t(row.meta.title)}，是否继续?`, '提示', {
		confirmButtonText: '删除',
		cancelButtonText: '取消',
		type: 'warning',
	})
		.then(async () => {
			for (const id of collectIds(row)) await api.remove('menus', id);
			await refreshFrontEndRoutes();
			ElMessage.success('删除成功');
			getTableData();
		})
		.catch(() => {});
};

onMounted(getTableData);
</script>
