using System;
using UnityEngine;

public class PlayerData
{
	public Action<Model.Type> ObserveMode_Listener;

	public int playerID;

	public string orignalCharacterName;

	public int rank;

	public int spawnCount;

	public bool playerViewModelVisible;

	public int zoomType;

	public Sprite zoomSprite;

	public float zoomCameraSpeedMultiplier;

	public bool isAbsorbed;

	public bool isBornNanoGhost;

	public int nanoDamage;

	public int nanoGhostLevel;

	public Action<int, int> nanoExp_Listener;

	public bool canPickUpWeapon;

	public bool ghostBladeSecKillTag;

	public SubscribeableProperty<int> kill;

	public SubscribeableProperty<int> death;

	public SubscribeableProperty<int> survival;

	public SubscribeableProperty<int> score;

	public SubscribeableProperty<HUD_Role.AceSign> aceSign;

	public SubscribeableProperty<NanoRole> nanoRole;

	public SubscribeableProperty<float> nanoRoleTableCloseTime;

	public Action<Player> revengeTarget_Listener;

	public Model.Type observeMode { get; private set; }

	public MultiKillTimer multiKillTimer { get; protected set; }

	public int nanoExp { get; private set; }

	public Player revengeTarget { get; private set; }

	public void SetObserveMode(Model.Type newMode)
	{
	}

	public void SetZoom(int type, Sprite sprite = null)
	{
	}

	public void SetNanoExp(int value)
	{
	}

	public void AddNanoExp(int value)
	{
	}

	public void SetRevengeTarget(Player killer)
	{
	}
}
