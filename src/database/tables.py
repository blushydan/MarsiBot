"""
File for storing Postgresql tables in sqlalchemy format
"""

import sqlalchemy as sa
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import ENUM


Base = declarative_base()


class Players(Base):
    __tablename__ = "players"
    id = sa.Column(sa.Integer, primary_key=True)
    discord_id = sa.Column(sa.Integer, nullable=False)
    game_id = sa.Column(
        sa.VARCHAR(30), sa.ForeignKey("game_instances.game_id"), nullable=False
    )
    role_id = sa.Column(sa.Integer, nullable=True)
    ghost_role_id = sa.Column(sa.Integer, nullable=True)
    money = sa.Column(sa.Integer, nullable=False)
    current_sanity = sa.Column(sa.Integer, nullable=False)
    current_visits_day = sa.Column(sa.Integer, nullable=False)
    current_visits_night = sa.Column(sa.Integer, nullable=False)
    current_location = sa.Column(
        sa.Integer, sa.ForeignKey("locations.id"), nullable=False
    )
    abilities_used = sa.Column(sa.JSON, nullable=True)


class ActiveAbilities(Base):
    __tablename__ = "active_abilities"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(50), nullable=False)
    description = sa.Column(sa.String(512), nullable=False)
    categories = sa.Column(sa.JSON)
    usage_limit = sa.Column(sa.JSON)
    phase = sa.Column(ENUM('Day', 'Night', 'Any'), nullable=False)
    type = sa.Column(ENUM('Physical', 'Remote'), nullable=False)
    forced_entry = sa.Column(sa.Boolean, default=False, nullable=False)
    target = sa.Column(sa.JSON)


class PassiveAbilities(Base):
    __tablename__ = "passive_abilities"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(50), nullable=False)
    description = sa.Column(sa.String(512), nullable=False)
    categories = sa.Column(sa.JSON)


class NormalRoles(Base):
    __tablename__ = "normal_roles"
    id = sa.Column(sa.Integer, primary_key=True)
    player_id = sa.Column(sa.Integer, sa.ForeignKey("players.id"))
    name = sa.Column(sa.String(128), nullable=False)


class GhostRoles(Base):
    __tablename__ = "ghost_roles"
    id = sa.Column(sa.Integer, primary_key=True)
    player_id = sa.Column(sa.Integer, sa.ForeignKey("players.id"))
    name = sa.Column(sa.String(128), nullable=False)


class GameInstances(Base):
    __tablename__ = "game_instances"
    game_id = sa.Column(sa.Integer, primary_key=True)
    created_at = sa.Column(sa.DateTime, nullable=False)
    server_id = sa.Column(sa.Integer, nullable=False)


# class GameStates(Base):
#     __tablename__ = "game_states"
#     state_id = sa.Column(sa.Integer, primary_key=True)
#     game_id = sa.Column(
#         sa.Integer, sa.ForeignKey("game_instances.game_id"), nullable=False
#     )
#     timestamp = sa.Column(sa.DateTime, nullable=False)
#     data = sa.Column(sa.JSON, nullable=False)


class Locations(Base):
    __tablename__ = "locations"
    id = sa.Column(sa.Integer, primary_key=True)
    game_id = sa.Column(
        sa.Integer, sa.ForeignKey("game_instances.game_id"), nullable=False
    )
    channel_id = sa.Column(sa.Integer, sa.ForeignKey("discord_channels.channel_id"), nullable=False)
    status = sa.Column(sa.String(128), nullable=True)
    meta_data = sa.Column(sa.JSON, nullable=False)


# class Paths(Base):
#     __tablename__ = "paths"
#     id = sa.Column(sa.Integer, primary_key=True)
#     phase = sa.Column(sa.VARCHAR(2), nullable=False)
#     house_start = sa.Column(sa.Integer, sa.ForeignKey("discord_channels.channel_id"), nullable=False)
#     house_end = sa.Column(sa.Integer, sa.ForeignKey("discord_channels.channel_id"), nullable=False)
#     channel_id = sa.Column(sa.Integer, sa.ForeignKey("discord_channels.channel_id"), nullable=False)


radio_location_association = sa.Table(
    'radio_location_association',
    Base.metadata,
    sa.Column('radio_channel_id', sa.Integer, sa.ForeignKey('radio_channels.id')),
    sa.Column('location_id', sa.Integer, sa.ForeignKey('locations.id'))
)


class RadioChannels(Base):
    __tablename__ = "radio_channels"
    id = sa.Column(sa.Integer, primary_key=True)
    frequency = sa.Column(sa.Float)
    active = sa.Column(sa.Boolean, default=True)

    locations = relationship(
        "Locations",
        secondary=radio_location_association,
        backref="radio_channels"
    )


class DiscordChannels(Base):
    __tablename__ = "discord_channels"
    channel_id = sa.Column(sa.Integer, primary_key=True)
    permissions = sa.Column(sa.JSON)
    type = sa.Column(sa.VARCHAR(45))


class StatusEffects(Base):
    __tablename__ = "status_effects"
    id = sa.Column(sa.Integer, primary_key=True)
    effect_name = sa.Column(sa.String(128), nullable=False)
    effect_data = sa.Column(sa.JSON, nullable=True)  # Additional data related to the effect, such as duration, etc.


class ObtainedStatusEffects(Base):
    __tablename__ = "obtained_status_effects"
    effect_id = sa.Column(sa.Integer, sa.ForeignKey("status_effects.id"), primary_key=True)
    player_id = sa.Column(sa.Integer, sa.ForeignKey("players.id"), primary_key=True)


class CommonItems(Base):
    __tablename__ = "common_items"
    id = sa.Column(sa.Integer, primary_key=True)
    item_name = sa.Column(sa.String(128), nullable=False)
    item_data = sa.Column(sa.JSON, nullable=True)  # Additional data related to the item


class InventoryItems(Base):
    __tablename__ = "inventory_items"
    item_id = sa.Column(sa.Integer, sa.ForeignKey("common_items.id"), primary_key=True, nullable=False)
    player_id = sa.Column(sa.Integer, sa.ForeignKey("players.id"), primary_key=True, nullable=False)


class ActiveAbilityUsage(Base):
    __tablename__ = "active_ability_usage"
    id = sa.Column(sa.Integer, primary_key=True)
    player_id = sa.Column(sa.Integer, sa.ForeignKey("players.id"), nullable=False)
    ability_id = sa.Column(sa.Integer, sa.ForeignKey("active_abilities.id"), nullable=False)
    location_used_on = sa.Column(sa.Integer, sa.ForeignKey("locations.id"), nullable=True)
    player_used_on = sa.Column(sa.Integer, sa.ForeignKey("players.id"), nullable=True)
    preset = sa.Column(sa.Boolean, nullable=False)
    preset_timestamp = sa.Column(sa.DateTime, nullable=True)
    timestamp = sa.Column(sa.DateTime, nullable=False)


class PassiveAbilityUsage(Base):
    __tablename__ = "passive_ability_usage"
    id = sa.Column(sa.Integer, primary_key=True)
    player_id = sa.Column(sa.Integer, sa.ForeignKey("players.id"), nullable=False)
    ability_id = sa.Column(sa.Integer, sa.ForeignKey("passive_abilities.id"), nullable=False)
    location_used_on = sa.Column(sa.Integer, sa.ForeignKey("locations.id"), nullable=True)
    player_used_on = sa.Column(sa.Integer, sa.ForeignKey("players.id"), nullable=True)
    preset = sa.Column(sa.Boolean, nullable=False)
    preset_timestamp = sa.Column(sa.DateTime, nullable=True)
    timestamp = sa.Column(sa.DateTime, nullable=False)


class Visits(Base):
    __tablename__ = "visits"
    id = sa.Column(sa.Integer, primary_key=True)
    player_id = sa.Column(sa.Integer, sa.ForeignKey("players.id"), nullable=False)
    location_id = sa.Column(sa.Integer, sa.ForeignKey("locations.id"), nullable=False)
    preset = sa.Column(sa.Boolean, nullable=False)
    preset_timestamp = sa.Column(sa.DateTime, nullable=True)
    timestamp = sa.Column(sa.DateTime, nullable=False)


class MoneyTransactions(Base):
    __tablename__ = "money_transactions"
    id = sa.Column(sa.Integer, primary_key=True)
    player_id_one = sa.Column(sa.Integer, sa.ForeignKey("players.id"), nullable=False)
    player_id_two = sa.Column(sa.Integer, sa.ForeignKey("players.id"), nullable=True)
    amount = sa.Column(sa.Integer, nullable=False)
    cause = sa.Column(sa.VARCHAR(60), nullable=False)
    timestamp = sa.Column(sa.DateTime, nullable=False)


class Deaths(Base):
    __tablename__ = "deaths"
    id = sa.Column(sa.Integer, primary_key=True)
    player_id = sa.Column(sa.Integer, sa.ForeignKey("players.id"), nullable=False)
    location_id = sa.Column(sa.Integer, sa.ForeignKey("locations.id"), nullable=True)
    timestamp = sa.Column(sa.DateTime, nullable=False)
