// 配置文件，用于切换不同的双重粤拼展示方案
const config = {
    // 展示方案：
    // 1: 方案A - 增加独立粤拼卡片
    // 2: 方案B - 卡片内部分区展示
    // 3: 方案C - 悬浮显示方案
    // 4: 方案D - 标签切换方案
    displayScheme: 3 // 默认使用方案C
};

// 导出配置
if (typeof module !== 'undefined' && module.exports) {
    module.exports = config;
} else {
    window.config = config;
}
