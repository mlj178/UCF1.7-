using CodeStage.AntiCheat.ObscuredTypes;

public class HealthData
{
	public ObscuredInt currentHealth;

	public ObscuredInt maxHealth;

	public ObscuredInt tempHealth;

	public float invinsibleEndTime;

	public float rate => 0f;

	public bool isDead => false;

	public bool isMaxHP => false;

	public HealthData(int maxHealth)
	{
	}

	public void Heal(int value)
	{
	}

	public void Heal()
	{
	}

	public void Hurt(int value)
	{
	}

	public void SetHealthMax(int value, bool heal = true)
	{
	}

	public void AddHealthMax(int addHP, bool heal = true)
	{
	}

	public void SetHealthMaxWithoutTempHealth(int value, bool heal = true)
	{
	}

	public void AddTempHealth(int addValue)
	{
	}

	public void ClearTempHealth()
	{
	}
}
