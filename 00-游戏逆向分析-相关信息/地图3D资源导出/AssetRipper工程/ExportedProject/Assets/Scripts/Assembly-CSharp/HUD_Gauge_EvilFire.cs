using UnityEngine;
using UnityEngine.UI;

public class HUD_Gauge_EvilFire : HUD_Gauge
{
	[SerializeField]
	private Color color1;

	[SerializeField]
	private Color color2;

	[SerializeField]
	private RawImage gaugeImage;

	[SerializeField]
	private GameObject gaugeLight;

	private bool useColor2;

	private float nextChangeColorTime;

	protected override void OnDisable()
	{
	}

	protected override void Update()
	{
	}

	public void Play(float maxPowerTime, float lastestShootTime)
	{
	}
}
