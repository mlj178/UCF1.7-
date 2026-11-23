using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using Cinemachine;
using CodeStage.AntiCheat.ObscuredTypes;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;

public class CameraManager : Singleton<CameraManager>
{
	[SerializeField]
	private CinemachineFreeLook freeLookCamera;

	private CinemachineBrain brain;

	public static ObscuredBool playerView;

	[CompilerGenerated]
	private static Action<Player, Player> m_FocusPlayerChangeEvent_Observers;

	private List<Camera> cameraStack;

	private float changeViewUnlockTime;

	private static VolumeProfile volumeProfile;

	private static GhostBladeOneShine oneShine;

	private static ThermalVision thermalVision;

	[SerializeField]
	private ForwardRendererData fwdRenderData;

	private ScriptableRendererFeature humanCatchFeature;

	public Player focusPlayer { get; private set; }

	private bool changeViewUnlock => false;

	public static event Action<Player, Player> FocusPlayerChangeEvent_Observers
	{
		[CompilerGenerated]
		add
		{
		}
		[CompilerGenerated]
		remove
		{
		}
	}

	protected override void Awake()
	{
	}

	private void Update()
	{
	}

	protected override void OnDestroy()
	{
	}

	public void ChangePVandCV()
	{
	}

	public void SetFocusPlayer(Player player)
	{
	}

	private void SpawnEvent(Player player)
	{
	}

	private void DeathEvent(DeathEventData data)
	{
	}

	public void SetFreeLookCameraActive(bool active)
	{
	}

	public void SetFreeLookCameraLookDir(Vector3 direction)
	{
	}

	public void TryChangeTeammateView(bool next)
	{
	}

	public static void PlayGhostBladeOneShineEffect()
	{
	}

	public static void SetThermalVision(float duration, bool showHuman)
	{
	}

	public static bool IsInThisPlayerPV(Entity entity)
	{
		return false;
	}

	public static void ManualUpdate()
	{
	}
}
