---
# PyQt6 Reusable Components Library

This library provides a collection of **polished, reusable PyQt6 widgets** for building desktop applications with consistent UI/UX.

---

## Table of Contents
- [Cards](#cards)
- [Navigation](#navigation)
- [Feedback & Information](#feedback--information)
- [Data & Visualization](#data--visualization)
- [User & Social](#user--social)
- [Form & Input](#form--input)
- [Utility](#utility)

---

## Cards

### `InfoCardWidget`
- **Description:** Displays a title, subtitle, and body text.
- **Use case:** Dashboard summaries, overviews.
- **Example:**
```python
card = InfoCardWidget(title="Total Users", subtitle="Active this month", description="1200 active users")
```

### `ProfileCardWidget`
- **Description:** Shows user avatar, name, role, and action buttons.
- **Use case:** User directories, team lists.
- **Example:**
```python
card = ProfileCardWidget(avatar="user.png", name="Alice", role="Designer")
```

### `StatCardWidget`
- **Description:** Displays a large number, label, and optional trend arrow.
- **Use case:** KPIs, metrics dashboard.
- **Example:**
```python
card = StatCardWidget(number=1500, label="Revenue", trend="up")
```

### `ExpandableCardWidget`
- **Description:** Collapsible card section.
- **Use case:** Detailed info on click.
- **Example:**
```python
card = ExpandableCardWidget(title="Orders")
card.add_content(widget)
```

### `HoverActionCardWidget`
- **Description:** Displays hidden action buttons on hover.
- **Use case:** Editable lists, dashboards.
- **Example:**
```python
card = HoverActionCardWidget(title="Project X")
```

### `ImageCardWidget`
- **Description:** Card with image preview and description.
- **Example:**
```python
card = ImageCardWidget(image_path="product.png", description="New product launch")
```

### `SelectableCardWidget`
- **Description:** Click-to-select card with highlight.
- **Example:**
```python
card = SelectableCardWidget(title="Option 1")
```

---

## Navigation

### `SidebarNavWidget`
- **Description:** Vertical navigation with icons and grouping.
- **Example:**
```python
sidebar = SidebarNavWidget(items=["Home", "Settings", "Profile"])
```

### `BreadcrumbBarWidget`
- **Description:** Clickable breadcrumb trail.
- **Example:**
```python
breadcrumbs = BreadcrumbBarWidget(paths=["Home", "Projects", "Project X"])
```

### `TabBarWidget`
- **Description:** Styled tab navigation with close buttons.
- **Example:**
```python
tabs = TabBarWidget(tabs=["Dashboard", "Reports"])
```

### `AccordionMenuWidget`
- **Description:** Collapsible menu sections.
- **Example:**
```python
accordion = AccordionMenuWidget(sections={"Settings": [...], "Users": [...]})
```

### `CommandPaletteWidget`
- **Description:** Quick searchable action palette.
- **Example:**
```python
palette = CommandPaletteWidget(actions=["Open File", "Save", "Close"])
```

### `PaginationWidget`
- **Description:** Numeric or infinite scroll pagination.
- **Example:**
```python
pagination = PaginationWidget(total_pages=10, current_page=1)
```

### `DockablePanelWidget`
- **Description:** Detachable, draggable panel.
- **Example:**
```python
dock = DockablePanelWidget(title="Console")
```

---

## Feedback & Information

### `NotificationToastWidget`
- **Description:** Small auto-dismissing popup.
- **Example:**
```python
toast = NotificationToastWidget(message="Saved successfully")
```

### `SnackbarWidget`
- **Description:** Bottom-floating message with action.
- **Example:**
```python
snackbar = SnackbarWidget(message="Item deleted", action_label="Undo")
```

### `StatusChipWidget`
- **Description:** Colored pill for status display.
- **Example:**
```python
chip = StatusChipWidget(text="Active", color="green")
```

### `BadgeLabel`
- **Description:** Label with count bubble.
- **Example:**
```python
badge = BadgeLabel(text="Messages", count=5)
```

### `ProgressOverlayWidget`
- **Description:** Semi-transparent overlay with spinner.
- **Example:**
```python
overlay = ProgressOverlayWidget(message="Loading...")
```

### `TooltipWidget`
- **Description:** Enhanced tooltip with icons or actions.
- **Example:**
```python
tooltip = TooltipWidget(text="Save changes")
```

### `EmptyStateWidget`
- **Description:** Friendly placeholder for empty data.
- **Example:**
```python
empty = EmptyStateWidget(message="No items found")
```

---

## Data & Visualization

### `DataTableWidget`
- **Description:** Table with sorting, filtering, pagination.
- **Example:**
```python
table = DataTableWidget(columns=["Name", "Role"], data=data_list)
```

### `TimelineWidget`
- **Description:** Vertical/horizontal chronological events.
- **Example:**
```python
timeline = TimelineWidget(events=[event1, event2])
```

### `KanbanBoardWidget`
- **Description:** Draggable task cards across columns.
- **Example:**
```python
kanban = KanbanBoardWidget(columns=["To Do", "In Progress", "Done"])
```

### `PropertyGridWidget`
- **Description:** Key-value editor for object properties.
- **Example:**
```python
grid = PropertyGridWidget(properties=obj_props)
```

### `MiniChartCard`
- **Description:** Inline chart inside card.
- **Example:**
```python
chart = MiniChartCard(data=[10, 20, 15, 30])
```

### `TreeViewWidget`
- **Description:** Hierarchical collapsible tree.
- **Example:**
```python
tree = TreeViewWidget(items=file_structure)
```

### `FileExplorerWidget`
- **Description:** Styled file/folder tree.
- **Example:**
```python
explorer = FileExplorerWidget(root_path="C:/Projects")
```

---

## User & Social

### `UserAvatarWidget`
- **Description:** Circular avatar with initials fallback.
- **Example:**
```python
avatar = UserAvatarWidget(image_path="user.png", initials="AL")
```

### `UserListItemWidget`
- **Description:** Avatar + name + subtitle + action buttons.
- **Example:**
```python
user_item = UserListItemWidget(name="Alice", role="Designer")
```

### `ChatBubbleWidget`
- **Description:** Left/right aligned message bubble.
- **Example:**
```python
bubble = ChatBubbleWidget(message="Hello", sender=True)
```

### `CommentThreadWidget`
- **Description:** Nested threaded comments.
- **Example:**
```python
thread = CommentThreadWidget(comments=comments_list)
```

### `RatingStarWidget`
- **Description:** Interactive star rating.
- **Example:**
```python
rating = RatingStarWidget(max_stars=5, value=3)
```

### `ReactionBarWidget`
- **Description:** Emoji/like reactions under content.
- **Example:**
```python
reactions = ReactionBarWidget(reactions=["👍", "❤️"])
```

### `ProfileHeaderWidget`
- **Description:** Banner + avatar + metadata.
- **Example:**
```python
header = ProfileHeaderWidget(name="Alice", role="Designer")
```

---

## Form & Input

### `SearchBoxWithSuggestions`
- **Description:** Live filter search box.
- **Example:**
```python
search = SearchBoxWithSuggestions(options=items_list)
```

### `InlineEditLabel`
- **Description:** Editable label on double-click.
- **Example:**
```python
editable = InlineEditLabel(text="Double-click to edit")
```

### `TagInputWidget`
- **Description:** Multi-select tags with chips.
- **Example:**
```python
tags = TagInputWidget(options=["Python", "Qt", "UI"])
```

### `RichTextEditorWidget`
- **Description:** Formatted text editor.
- **Example:**
```python
editor = RichTextEditorWidget()
```

### `FormStepperWidget`
- **Description:** Multi-step wizard with validation.
- **Example:**
```python
stepper = FormStepperWidget(steps=[step1, step2, step3])
```

### `DateRangePickerWidget`
- **Description:** Select start and end dates.
- **Example:**
```python
date_picker = DateRangePickerWidget()
```

### `ToggleSwitchWidget`
- **Description:** Modern on/off switch.
- **Example:**
```python
toggle = ToggleSwitchWidget(state=True)
```

### `SliderWithInputWidget`
- **Description:** Slider with numeric input.
- **Example:**
```python
slider = SliderWithInputWidget(min=0, max=100, value=50)
```

---

## Utility

### `FloatingActionButton`
- **Description:** Circular quick action button.
- **Example:**
```python
fab = FloatingActionButton(icon="add")
```

### `QuickSettingsPanel`
- **Description:** System-style toggle panel.
- **Example:**
```python
settings = QuickSettingsPanel(toggles=[toggle1, toggle2])
```

### `PinnedNoteWidget`
- **Description:** Sticky note annotation.
- **Example:**
```python
note = PinnedNoteWidget(text="Remember this")
```

### `ClipboardHistoryWidget`
- **Description:** Shows previous clipboard items.
- **Example:**
```python
clipboard = ClipboardHistoryWidget(items=clip_items)
```

### `GlobalSearchWidget`
- **Description:** Unified search across app content.
- **Example:**
```python
search = GlobalSearchWidget(data_sources=[data1, data2])
```

### `ShortcutHelperWidget`
- **Description:** Overlay showing keyboard shortcuts.
- **Example:**
```python
sho