class Texts:
    # message
    START_NEW_USER = "✅ Ваш запрос отправлен администратору. Ожидайте активации. ⏳"
    START_EXISTING_USER = "👋 Добро пожаловать! Вы уже зарегистрированы."
    INACTIVE_USERS = "Список неактивированных пользователей\nПо нажатию Активация"
    ACTIVE_USERS = "Список пользователей\nПо нажатию вывод информации"
    BEGIN = "Начало"
    ADMIN_PANEL = "⚙️ Админ панель"
    
    # buttons
    BTN_PROFILE = "👤 Профиль"
    BTN_TEMPERATURE = "🌡 Температура"
    BTN_TEMPERATURE_GRAPH = "📊 График температуры"
    BTN_STATUS = "ℹ️ Статус"
    BTN_ADMIN_PANEL = "⚙️ Админ панель"
    BTN_ALL_USERS = "👥 Все пользователи"
    BTN_INACTIVE_USERS = "🛑 Неактивные пользователи"
    BTN_BACK = "🔙 Назад"
    
    
    SELECT_PERIOD = "📅 Выберите период:"
    GRAPH_CAPTION = "📈 График за последние {hours} часов"
    PERIODS = {
        "🕐 1 час": 1,
        "🕕 6 часов": 6,
        "📆 Сутки": 24,
        "📅 Неделя": 168,
        "🗓 Месяц": 720
    }