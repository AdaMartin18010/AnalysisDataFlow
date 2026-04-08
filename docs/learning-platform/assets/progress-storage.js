/**
 * AnalysisDataFlow 学习平台 - 进度存储管理
 * 使用 localStorage 实现本地数据持久化
 */

class ProgressStorage {
    constructor() {
        this.storageKey = 'adf_learning_progress';
        this.userKey = 'adf_user_profile';
        this.achievementsKey = 'adf_achievements';
        this.notificationsKey = 'adf_notifications';
        this.init();
    }

    // 初始化存储
    init() {
        if (!this.getData()) {
            this.resetData();
        }
        if (!this.getUserProfile()) {
            this.resetUserProfile();
        }
        if (!this.getAchievements()) {
            this.resetAchievements();
        }
    }

    // 获取所有数据
    getData() {
        try {
            const data = localStorage.getItem(this.storageKey);
            return data ? JSON.parse(data) : null;
        } catch (e) {
            console.error('Error reading from localStorage:', e);
            return null;
        }
    }

    // 保存数据
    saveData(data) {
        try {
            localStorage.setItem(this.storageKey, JSON.stringify(data));
            return true;
        } catch (e) {
            console.error('Error saving to localStorage:', e);
            return false;
        }
    }

    // 重置数据
    resetData() {
        const initialData = {
            version: '1.0',
            lastUpdated: new Date().toISOString(),
            courses: {},
            labs: {},
            challenges: {},
            quizzes: {},
            certifications: {
                csa: { progress: 0, completed: false, score: 0 },
                csp: { progress: 0, completed: false, score: 0 },
                cse: { progress: 0, completed: false, score: 0 }
            },
            studyTime: 0, // 分钟
            streakDays: 0,
            lastStudyDate: null,
            totalXP: 0
        };
        this.saveData(initialData);
        return initialData;
    }

    // 获取用户档案
    getUserProfile() {
        try {
            const data = localStorage.getItem(this.userKey);
            return data ? JSON.parse(data) : null;
        } catch (e) {
            console.error('Error reading user profile:', e);
            return null;
        }
    }

    // 保存用户档案
    saveUserProfile(profile) {
        try {
            localStorage.setItem(this.userKey, JSON.stringify(profile));
            return true;
        } catch (e) {
            console.error('Error saving user profile:', e);
            return false;
        }
    }

    // 重置用户档案
    resetUserProfile() {
        const initialProfile = {
            name: '学习者',
            email: '',
            avatar: null,
            goal: 'beginner',
            weeklyGoal: 5, // 小时
            joinDate: new Date().toISOString(),
            preferences: {
                theme: 'light',
                editorTheme: 'vs',
                autoSave: true,
                studyReminder: true
            }
        };
        this.saveUserProfile(initialProfile);
        return initialProfile;
    }

    // 获取成就
    getAchievements() {
        try {
            const data = localStorage.getItem(this.achievementsKey);
            return data ? JSON.parse(data) : null;
        } catch (e) {
            console.error('Error reading achievements:', e);
            return null;
        }
    }

    // 保存成就
    saveAchievements(achievements) {
        try {
            localStorage.setItem(this.achievementsKey, JSON.stringify(achievements));
            return true;
        } catch (e) {
            console.error('Error saving achievements:', e);
            return false;
        }
    }

    // 重置成就
    resetAchievements() {
        const initialAchievements = {};
        this.saveAchievements(initialAchievements);
        return initialAchievements;
    }

    // 解锁成就
    unlockAchievement(achievementId) {
        const achievements = this.getAchievements();
        if (!achievements[achievementId]) {
            achievements[achievementId] = {
                unlockedAt: new Date().toISOString(),
                viewed: false
            };
            this.saveAchievements(achievements);
            
            // 添加通知
            this.addNotification({
                type: 'achievement',
                title: '获得新成就！',
                message: this.getAchievementName(achievementId),
                icon: 'fa-trophy'
            });
            
            return true;
        }
        return false;
    }

    // 获取成就名称
    getAchievementName(achievementId) {
        const achievementMap = {
            'first-login': '初次见面',
            'first-course': '开始学习',
            'first-lab': '动手实践',
            'first-challenge': '编程新手',
            'perfect-quiz': '满分学霸',
            'study-streak-7': '坚持不懈',
            'csa-certified': 'CSA 认证',
            'csp-certified': 'CSP 认证',
            'cse-certified': 'CSE 认证'
        };
        return achievementMap[achievementId] || achievementId;
    }

    // 获取通知
    getNotifications() {
        try {
            const data = localStorage.getItem(this.notificationsKey);
            return data ? JSON.parse(data) : [];
        } catch (e) {
            console.error('Error reading notifications:', e);
            return [];
        }
    }

    // 添加通知
    addNotification(notification) {
        const notifications = this.getNotifications();
        notifications.unshift({
            id: Date.now(),
            timestamp: new Date().toISOString(),
            read: false,
            ...notification
        });
        // 限制通知数量
        if (notifications.length > 50) {
            notifications.pop();
        }
        localStorage.setItem(this.notificationsKey, JSON.stringify(notifications));
        return notifications;
    }

    // 标记通知已读
    markNotificationsRead() {
        const notifications = this.getNotifications();
        notifications.forEach(n => n.read = true);
        localStorage.setItem(this.notificationsKey, JSON.stringify(notifications));
    }

    // 清除通知
    clearNotifications() {
        localStorage.setItem(this.notificationsKey, JSON.stringify([]));
    }

    // 课程进度
    getCourseProgress(courseId) {
        const data = this.getData();
        return data.courses[courseId] || { completed: false, progress: 0, lessons: {} };
    }

    updateCourseProgress(courseId, lessonId, completed = true) {
        const data = this.getData();
        if (!data.courses[courseId]) {
            data.courses[courseId] = { completed: false, progress: 0, lessons: {} };
        }
        
        data.courses[courseId].lessons[lessonId] = {
            completed,
            completedAt: new Date().toISOString()
        };

        // 计算课程进度
        const course = coursesData.courses.find(c => c.id === courseId);
        if (course) {
            const completedLessons = Object.values(data.courses[courseId].lessons).filter(l => l.completed).length;
            data.courses[courseId].progress = Math.round((completedLessons / course.lessons) * 100);
            data.courses[courseId].completed = completedLessons === course.lessons;
        }

        data.lastUpdated = new Date().toISOString();
        this.saveData(data);
        this.updateStudyTime(15); // 假设每课15分钟
        this.updateStreak();
        
        // 检查成就
        this.checkAchievements();
        
        return data.courses[courseId];
    }

    // 实验进度
    getLabProgress(labId) {
        const data = this.getData();
        return data.labs[labId] || { completed: false, tasks: {} };
    }

    updateLabProgress(labId, taskIndex, completed = true) {
        const data = this.getData();
        if (!data.labs[labId]) {
            data.labs[labId] = { completed: false, tasks: {} };
        }
        
        data.labs[labId].tasks[taskIndex] = {
            completed,
            completedAt: new Date().toISOString()
        };

        // 检查是否所有任务完成
        const lab = coursesData.labs.find(l => l.id === labId);
        if (lab) {
            const completedTasks = Object.values(data.labs[labId].tasks).filter(t => t.completed).length;
            data.labs[labId].completed = completedTasks === lab.tasks.length;
        }

        data.lastUpdated = new Date().toISOString();
        this.saveData(data);
        this.updateStudyTime(60); // 假设每个实验60分钟
        this.updateStreak();
        this.checkAchievements();
        
        return data.labs[labId];
    }

    // 挑战进度
    getChallengeProgress(challengeId) {
        const data = this.getData();
        return data.challenges[challengeId] || { completed: false, attempts: 0, bestScore: 0 };
    }

    updateChallengeProgress(challengeId, completed, score = 0) {
        const data = this.getData();
        if (!data.challenges[challengeId]) {
            data.challenges[challengeId] = { completed: false, attempts: 0, bestScore: 0 };
        }
        
        data.challenges[challengeId].attempts++;
        if (score > data.challenges[challengeId].bestScore) {
            data.challenges[challengeId].bestScore = score;
        }
        if (completed) {
            data.challenges[challengeId].completed = true;
            data.challenges[challengeId].completedAt = new Date().toISOString();
        }

        data.lastUpdated = new Date().toISOString();
        this.saveData(data);
        this.updateStudyTime(120); // 假设每个挑战120分钟
        this.updateStreak();
        this.checkAchievements();
        
        return data.challenges[challengeId];
    }

    // 测验结果
    getQuizResult(quizId) {
        const data = this.getData();
        return data.quizzes[quizId] || null;
    }

    saveQuizResult(quizId, score, totalQuestions, answers) {
        const data = this.getData();
        const passed = score >= (coursesData.quizzes.find(q => q.id === quizId)?.passingScore || 70);
        
        data.quizzes[quizId] = {
            score,
            totalQuestions,
            passed,
            answers,
            completedAt: new Date().toISOString(),
            attempts: (data.quizzes[quizId]?.attempts || 0) + 1
        };

        data.lastUpdated = new Date().toISOString();
        this.saveData(data);
        this.updateStudyTime(30); // 假设每次测验30分钟
        this.updateStreak();
        
        // 检查是否满分
        if (score === 100) {
            this.unlockAchievement('perfect-quiz');
        }
        
        this.checkAchievements();
        return data.quizzes[quizId];
    }

    // 更新学习时长（分钟）
    updateStudyTime(minutes) {
        const data = this.getData();
        data.studyTime += minutes;
        data.totalXP += Math.floor(minutes / 10); // 每10分钟1 XP
        data.lastUpdated = new Date().toISOString();
        this.saveData(data);
    }

    // 更新连续学习天数
    updateStreak() {
        const data = this.getData();
        const today = new Date().toDateString();
        const lastDate = data.lastStudyDate ? new Date(data.lastStudyDate).toDateString() : null;
        
        if (lastDate !== today) {
            const yesterday = new Date();
            yesterday.setDate(yesterday.getDate() - 1);
            
            if (lastDate === yesterday.toDateString()) {
                // 连续学习
                data.streakDays++;
            } else {
                // 中断后重新开始
                data.streakDays = 1;
            }
            
            data.lastStudyDate = new Date().toISOString();
            data.lastUpdated = new Date().toISOString();
            this.saveData(data);
            
            // 检查连续学习成就
            if (data.streakDays >= 7) {
                this.unlockAchievement('study-streak-7');
            }
        }
    }

    // 检查成就
    checkAchievements() {
        const data = this.getData();
        
        // 检查第一个课程
        if (!this.getAchievements()['first-course']) {
            const hasCompletedCourse = Object.values(data.courses).some(c => c.completed);
            if (hasCompletedCourse) {
                this.unlockAchievement('first-course');
            }
        }
        
        // 检查第一个实验
        if (!this.getAchievements()['first-lab']) {
            const hasCompletedLab = Object.values(data.labs).some(l => l.completed);
            if (hasCompletedLab) {
                this.unlockAchievement('first-lab');
            }
        }
        
        // 检查第一个挑战
        if (!this.getAchievements()['first-challenge']) {
            const hasCompletedChallenge = Object.values(data.challenges).some(c => c.completed);
            if (hasCompletedChallenge) {
                this.unlockAchievement('first-challenge');
            }
        }
        
        // 检查认证成就
        if (data.certifications.csa.completed) {
            this.unlockAchievement('csa-certified');
        }
        if (data.certifications.csp.completed) {
            this.unlockAchievement('csp-certified');
        }
        if (data.certifications.cse.completed) {
            this.unlockAchievement('cse-certified');
        }
    }

    // 更新认证进度
    updateCertificationProgress(certId, progress) {
        const data = this.getData();
        if (data.certifications[certId]) {
            data.certifications[certId].progress = progress;
            data.lastUpdated = new Date().toISOString();
            this.saveData(data);
        }
        return data.certifications[certId];
    }

    completeCertification(certId, score) {
        const data = this.getData();
        if (data.certifications[certId]) {
            data.certifications[certId].completed = true;
            data.certifications[certId].score = score;
            data.certifications[certId].completedAt = new Date().toISOString();
            data.lastUpdated = new Date().toISOString();
            this.saveData(data);
            this.checkAchievements();
        }
        return data.certifications[certId];
    }

    // 获取统计数据
    getStats() {
        const data = this.getData();
        const profile = this.getUserProfile();
        
        return {
            studyTime: Math.floor(data.studyTime / 60), // 转换为小时
            completedCourses: Object.values(data.courses).filter(c => c.completed).length,
            completedLabs: Object.values(data.labs).filter(l => l.completed).length,
            completedChallenges: Object.values(data.challenges).filter(c => c.completed).length,
            totalScore: Object.values(data.quizzes).reduce((sum, q) => sum + q.score, 0),
            streakDays: data.streakDays,
            totalXP: data.totalXP,
            name: profile?.name || '学习者',
            level: this.calculateLevel(data.totalXP)
        };
    }

    // 计算等级
    calculateLevel(xp) {
        if (xp < 100) return '初级学员';
        if (xp < 300) return '进阶学员';
        if (xp < 600) return '高级学员';
        if (xp < 1000) return '流计算达人';
        return '流计算专家';
    }

    // 获取学习进度（用于仪表盘）
    getLearningProgress() {
        const data = this.getData();
        const progress = [];
        
        // 课程进度
        coursesData.courses.forEach(course => {
            const courseProgress = data.courses[course.id];
            if (courseProgress && courseProgress.progress > 0) {
                progress.push({
                    type: 'course',
                    id: course.id,
                    title: course.title,
                    progress: courseProgress.progress,
                    icon: course.icon,
                    lastAccessed: courseProgress.lastAccessed
                });
            }
        });
        
        // 按进度排序
        progress.sort((a, b) => b.progress - a.progress);
        return progress.slice(0, 5);
    }

    // 导出数据
    exportData() {
        return {
            progress: this.getData(),
            profile: this.getUserProfile(),
            achievements: this.getAchievements(),
            exportedAt: new Date().toISOString()
        };
    }

    // 导入数据
    importData(data) {
        if (data.progress) {
            this.saveData(data.progress);
        }
        if (data.profile) {
            this.saveUserProfile(data.profile);
        }
        if (data.achievements) {
            this.saveAchievements(data.achievements);
        }
        return true;
    }

    // 清除所有数据
    clearAll() {
        localStorage.removeItem(this.storageKey);
        localStorage.removeItem(this.userKey);
        localStorage.removeItem(this.achievementsKey);
        localStorage.removeItem(this.notificationsKey);
        this.init();
    }
}

// 创建全局实例
const storage = new ProgressStorage();
