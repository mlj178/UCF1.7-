using System;
using Cinemachine;
using UnityEngine;

public class PlayerCameraManager : MonoBehaviour
{
	public struct FovZoomInfo
	{
		public Buff bindBuff;

		public float extraMapFov;

		public float extraPvFov;

		public float inTime;

		public float outTime;

		public FovZoomInfo(Buff bindBuff, float extraMapFov, float extraPvFov, float inTime, float outTime)
		{
			this.bindBuff = null;
			this.extraMapFov = 0f;
			this.extraPvFov = 0f;
			this.inTime = 0f;
			this.outTime = 0f;
		}
	}

	[SerializeField]
	private CinemachineVirtualCamera mapCamera;

	public Camera modelCamera;

	private int activeCullingMask;

	public Transform modelContainer;

	private Vector3 modelDelayPos;

	private float zoomFovScale;

	private string zoomAnimId;

	private string skillZoomId;

	private float knifeHit_Value;

	private Coroutine knifeHit_Coroutine;

	private static readonly Vector3 modelRightHandScale;

	public const float defaultFOV = 67.51225f;

	public float modelDefaultFOV;

	private float extraMapFov;

	private float extraPvFov;

	private FovZoomInfo fovZoomInfo;

	public Transform modelCameraTransform => null;

	private float mapFOV
	{
		set
		{
		}
	}

	private float modelFOV
	{
		set
		{
		}
	}

	public bool modelVisible
	{
		set
		{
		}
	}

	public bool focus
	{
		set
		{
		}
	}

	private void Awake()
	{
	}

	private void Update()
	{
	}

	private void OnDestroy()
	{
	}

	private void SetModelDelayPos()
	{
	}

	public void AddModelDelayPos(float delay)
	{
	}

	public void PlaySniperZoom(float fovScale, float duration, Action endCallBack)
	{
	}

	private void CameraFovSetting()
	{
	}

	public void SetRotation(float angle)
	{
	}

	public void LookAt(Vector3 dir)
	{
	}

	public void PlayKnifeHitStunShake(bool isBigshot)
	{
	}

	public void SetFovBuffInfo(FovZoomInfo info)
	{
	}

	private void FovZommBuffEndEvent()
	{
	}
}
