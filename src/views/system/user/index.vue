<template>
	<div class="system-user-container layout-padding">
		<aside class="unit-panel">
			<div class="unit-panel-head">
				<div class="unit-panel-title"><el-icon><ele-OfficeBuilding /></el-icon><span>单位目录</span></div>
				<div class="unit-panel-sub">共 {{ state.units.length }} 个单位</div>
			</div>
			<div class="unit-search">
				<el-input v-model="state.unitSearch" size="default" placeholder="搜索单位名称" clearable :prefix-icon="SearchIcon" />
			</div>
			<div class="unit-scroll">
				<div class="unit-all" :class="{ 'is-active': state.selectedUnitId === null }" @click="onSelectAll">
					<span class="unit-all-icon"><el-icon><ele-FolderOpened /></el-icon></span>
					<span class="unit-all-label">全部单位</span>
					<span class="unit-all-count">{{ allUserCount }}</span>
				</div>
				<div class="unit-divider"></div>
				<el-tree
					ref="treeRef"
					:data="state.units"
					node-key="id"
					:props="{ label: 'deptName' }"
					highlight-current
					:current-node-key="state.selectedUnitId ?? undefined"
					:filter-node-method="filterUnitNode"
					:expand-on-click-node="false"
					empty-text="暂无单位"
					@node-click="onUnitClick"
				>
					<template #default="{ data }">
						<div class="unit-node">
							<span class="unit-node-icon"><el-icon><ele-OfficeBuilding /></el-icon></span>
							<span class="unit-node-label">{{ data.deptName }}</span>
							<span class="unit-node-count">{{ state.unitCounts[data.id] || 0 }}</span>
						</div>
					</template>
				</el-tree>
			</div>
		</aside>

		<div class="system-user-main layout-padding-view layout-padding-auto">
			<div class="user-toolbar">
				<div class="user-toolbar-left">
					<el-input v-model="state.search" placeholder="请输入用户名称" clearable style="max-width: 180px" />
					<el-button type="primary" class="ml10" @click="onSearch">查询</el-button>
					<el-button type="success" class="ml10" @click="onAdd">新增用户</el-button>
				</div>
				<el-tag class="current-dept-tag" type="primary" effect="light" round>
					<el-icon><ele-LocationInformation /></el-icon>
					当前部门：{{ currentUnitName }}
				</el-tag>
			</div>
			<div v-if="state.selectedUnitId !== null && state.tableData.config.total === 0 && !state.tableData.loading" class="empty-hint">
				当前部门暂无人员，可切换到「全部单位」查看其它人员
			</div>
			<Table
				ref="tableRef"
				:data="state.tableData.data"
				:header="state.tableData.header"
				:config="state.tableData.config"
				class="system-user-table"
				@delRow="onDelRow"
				@editRow="onEditRow"
				@pageChange="onPageChange"
				@sortHeader="onSortHeader"
			/>
			<UserDialog
				v-model="state.dialogVisible"
				:initial="state.editing"
				:units="state.units"
				:roles="state.roles"
				@submit="onDialogSubmit"
			/>
		</div>
	</div>
</template>

<script setup lang="ts" name="systemUser">
import { defineAsyncComponent, reactive, ref, computed, watch, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { Search as SearchIcon } from '@element-plus/icons-vue';
import { useBusinessCrud } from '/@/utils/businessCrud';
import { refreshFrontEndRoutes } from '/@/router/frontEnd';

const Table = defineAsyncComponent(() => import('/@/components/table/index.vue'));
const UserDialog = defineAsyncComponent(() => import('/@/views/system/user/dialog.vue'));

const crud = useBusinessCrud('users');
const tableRef = ref<RefType>();
const treeRef = ref();
const state = reactive<
	BusinessTableState & {
		search: string;
		unitSearch: string;
		selectedUnitId: number | null;
		unitCounts: Record<number, number>;
		dialogVisible: boolean;
		editing: EmptyObjectType;
		units: EmptyObjectType[];
		roles: EmptyObjectType[];
	}
>({
	search: '',
	unitSearch: '',
	selectedUnitId: null,
	unitCounts: {},
	dialogVisible: false,
	editing: {},
	units: [],
	roles: [],
	tableData: {
		data: [],
		header: [
			{ key: 'userName', colWidth: '', title: '用户名', type: 'text', width: '', isCheck: true },
			{ key: 'realName', colWidth: '', title: '姓名', type: 'text', width: '', isCheck: true },
			{ key: 'phone', colWidth: '', title: '手机号', type: 'text', width: '', isCheck: true },
			{ key: 'statusText', colWidth: '', title: '用户状态', type: 'text', width: '', isCheck: true },
		],
		config: {
			total: 0,
			loading: false,
			isBorder: false,
			isSelection: false,
			isSerialNo: true,
			isOperate: true,
			isEdit: true,
			disableDeleteConfirm: true,
		},
		search: [],
		param: { pageNum: 1, pageSize: 10 },
	},
});

const allUserCount = computed(() => Object.values(state.unitCounts).reduce((sum, n) => sum + n, 0));
const currentUnitName = computed(() => {
	if (state.selectedUnitId === null) return '全部部门';
	return state.units.find((u: EmptyObjectType) => u.id === state.selectedUnitId)?.deptName || '未知部门';
});

const loadUnitCounts = async () => {
	const res = await crud.api.list('users');
	const counts: Record<number, number> = {};
	((res.data as any[]) || []).forEach((u) => {
		if (u.unitId != null) counts[u.unitId] = (counts[u.unitId] || 0) + 1;
	});
	state.unitCounts = counts;
};

const getTableData = async () => {
	state.tableData.loading = true;
	try {
		const params: Record<string, any> = { ...state.tableData.param, keyword: state.search };
		if (state.selectedUnitId !== null) params.unitId = state.selectedUnitId;
		const { rows, total } = await crud.page(params);
		state.tableData.data = rows.map((row) => ({ ...row, statusText: row.status ? '启用' : '禁用' }));
		state.tableData.config.total = total;
	} finally {
		state.tableData.loading = false;
	}
};

const onUnitClick = (data: EmptyObjectType) => {
	state.selectedUnitId = data.id;
	state.tableData.param.pageNum = 1;
	getTableData();
};
const onSelectAll = () => {
	state.selectedUnitId = null;
	treeRef.value?.setCurrentKey(undefined);
	state.tableData.param.pageNum = 1;
	getTableData();
};
const filterUnitNode = (value: string, data: EmptyObjectType) => {
	if (!value) return true;
	return (data.deptName || '').toLowerCase().includes(value.toLowerCase()) || (data.deptShortName || '').toLowerCase().includes(value.toLowerCase());
};
watch(() => state.unitSearch, (val) => treeRef.value?.filter(val));

const onSearch = () => {
	state.tableData.param.pageNum = 1;
	tableRef.value?.pageReset();
	getTableData();
};
const onPageChange = (page: TableDemoPageType) => {
	state.tableData.param.pageNum = page.pageNum;
	state.tableData.param.pageSize = page.pageSize;
	getTableData();
};
const onSortHeader = (data: TableHeaderType[]) => {
	state.tableData.header = data;
};
const onAdd = () => {
	state.editing = { unitId: state.selectedUnitId ?? undefined };
	state.dialogVisible = true;
};
const onEditRow = (row: EmptyObjectType) => {
	state.editing = { ...row };
	state.dialogVisible = true;
};
const onDialogSubmit = async (form: EmptyObjectType) => {
	await crud.submit(form);
	await loadUnitCounts();
	await refreshFrontEndRoutes();
	getTableData();
};
const onDelRow = async (row: EmptyObjectType) => {
	if (row.userName === 'admin') {
		ElMessage.warning('管理员账号不可删除');
		return;
	}
	try {
		await crud.remove(row, `用户 ${row.userName}`);
		await loadUnitCounts();
		await refreshFrontEndRoutes();
		getTableData();
	} catch {
		// 用户取消删除
	}
};

onMounted(async () => {
	const [units, roles] = await Promise.all([crud.api.list('units'), crud.api.list('roles')]);
	state.units = (units.data as any[]) || [];
	state.roles = (roles.data as any[]) || [];
	await loadUnitCounts();
	getTableData();
});
</script>

<style scoped lang="scss">
.system-user-container.layout-padding {
	display: flex;
	flex-direction: row;
	height: 100%;
	gap: 15px;

	.unit-panel {
		width: 250px;
		flex-shrink: 0;
		display: flex;
		flex-direction: column;
		background: var(--el-bg-color);
		border: 1px solid var(--el-border-color-lighter);
		border-radius: 10px;
		box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
		overflow: hidden;
		transition: box-shadow 0.25s ease;
		&:hover {
			box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
		}
		.unit-panel-head {
			padding: 16px 16px 14px;
			background: linear-gradient(135deg, var(--el-color-primary-light-9) 0%, var(--el-bg-color) 100%);
			border-bottom: 1px solid var(--el-border-color-lighter);
			.unit-panel-title {
				display: flex;
				align-items: center;
				gap: 8px;
				font-size: 16px;
				font-weight: 600;
				color: var(--el-text-color-primary);
				.el-icon {
					color: var(--el-color-primary);
					font-size: 18px;
				}
			}
			.unit-panel-sub {
				margin-top: 6px;
				padding-left: 26px;
				font-size: 12px;
				color: var(--el-text-color-secondary);
			}
		}
		.unit-search {
			padding: 12px 12px 8px;
		}
		.unit-scroll {
			flex: 1;
			min-height: 0;
			overflow-y: auto;
			padding: 0 8px 12px;
			.unit-all,
			:deep(.el-tree-node__content) {
				height: 38px;
				border-radius: 8px;
				transition: background 0.2s ease;
			}
			.unit-all {
				display: flex;
				align-items: center;
				gap: 10px;
				padding: 0 10px;
				margin: 2px 0;
				cursor: pointer;
				color: var(--el-text-color-regular);
				font-size: 14px;
				&:hover {
					background: var(--el-fill-color-light);
				}
				&.is-active {
					background: var(--el-color-primary-light-9);
					color: var(--el-color-primary);
					font-weight: 500;
				}
				.unit-all-icon {
					width: 24px;
					height: 24px;
					display: flex;
					align-items: center;
					justify-content: center;
					border-radius: 6px;
					background: var(--el-fill-color);
					font-size: 14px;
				}
				&.is-active .unit-all-icon {
					background: var(--el-color-primary);
					color: #fff;
				}
				.unit-all-label {
					flex: 1;
				}
				.unit-all-count,
				.unit-node-count {
					min-width: 20px;
					padding: 1px 7px;
					border-radius: 10px;
					background: var(--el-fill-color);
					font-size: 12px;
					text-align: center;
					color: var(--el-text-color-secondary);
				}
			}
			.unit-divider {
				height: 1px;
				margin: 6px 10px;
				background: var(--el-border-color-lighter);
			}
			:deep(.el-tree) {
				background: transparent;
				.el-tree-node__content:hover {
					background: var(--el-fill-color-light);
				}
				.el-tree-node.is-current > .el-tree-node__content {
					background: var(--el-color-primary-light-9);
				}
			}
			.unit-node {
				display: flex;
				align-items: center;
				gap: 10px;
				width: 100%;
				padding-right: 8px;
				font-size: 14px;
				.unit-node-icon {
					width: 24px;
					height: 24px;
					display: flex;
					align-items: center;
					justify-content: center;
					border-radius: 6px;
					background: var(--el-color-primary-light-9);
					color: var(--el-color-primary);
					font-size: 14px;
				}
				.unit-node-label {
					flex: 1;
					overflow: hidden;
					text-overflow: ellipsis;
					white-space: nowrap;
				}
			}
		}
	}

	.system-user-main {
		flex: 1;
		min-width: 0;
		display: flex;
		flex-direction: column;
		padding: 15px;
		background: var(--el-bg-color);
		border: 1px solid var(--el-border-color-lighter);
		border-radius: 10px;
		box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
		.user-toolbar {
			display: flex;
			align-items: center;
			justify-content: space-between;
			gap: 12px;
			.user-toolbar-left {
				display: flex;
				align-items: center;
			}
			.current-dept-tag {
				.el-icon {
					margin-right: 4px;
				}
			}
		}
		.empty-hint {
			margin: 10px 0;
			padding: 10px 14px;
			border-radius: 8px;
			background: var(--el-color-info-light-9);
			color: var(--el-text-color-secondary);
			font-size: 13px;
		}
		.system-user-table {
			flex: 1;
			overflow: hidden;
		}
	}
}
</style>
